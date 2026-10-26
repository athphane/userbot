"""A small SQLite document store for the collection calls used by this bot.

This deliberately supports a subset of the former driver: equality filters,
string $regex searches, top-level projections, $set/$inc/$unset, and upserts.
Unsupported operators raise instead of silently changing query semantics.
"""

import json
import re
import sqlite3
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from threading import RLock
from typing import Any, Iterator, Optional, Union
from uuid import uuid4


@dataclass(frozen=True)
class InsertOneResult:
    inserted_id: Any


@dataclass(frozen=True)
class UpdateResult:
    matched_count: int
    modified_count: int
    upserted_id: Any = None


@dataclass(frozen=True)
class DeleteResult:
    deleted_count: int


def _pack(document: dict) -> tuple:
    """Encode datetimes separately so ordinary JSON objects round-trip unchanged."""
    dates = []

    def encode(value, path):
        if isinstance(value, datetime):
            dates.append(path)
            return value.isoformat()
        if isinstance(value, dict):
            if not all(isinstance(key, str) for key in value):
                raise TypeError("Document keys must be strings")
            return {key: encode(item, path + [key]) for key, item in value.items()}
        if isinstance(value, list):
            return [encode(item, path + [index]) for index, item in enumerate(value)]
        return value

    return (
        json.dumps(encode(document, []), separators=(",", ":"), allow_nan=False),
        json.dumps(dates),
    )


def _unpack(document: str, dates: str) -> dict:
    """Restore datetime values, including those in nested objects and arrays."""
    result = json.loads(document)
    for path in json.loads(dates):
        parent = result
        for key in path[:-1]:
            parent = parent[key]
        parent[path[-1]] = datetime.fromisoformat(parent[path[-1]])
    return result


def _field(field: str) -> str:
    """Build a safe JSON path; values and collection names are always bound."""
    if not isinstance(field, str) or not re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*", field
    ):
        raise NotImplementedError(f"Unsupported query field: {field!r}")
    return f"'$.{field}'"


def _where(query: Optional[dict]) -> tuple:
    """Compile equality and regex filters into parameterized SQLite queries."""
    clauses, parameters = [], []
    if query is not None and not isinstance(query, dict):
        raise TypeError("A filter must be a dictionary")
    for field, value in (query or {}).items():
        path = _field(field)
        expression = f"json_extract(document, {path})"
        if isinstance(value, dict) and any(key.startswith("$") for key in value):
            if "$regex" not in value or set(value) - {"$regex", "$options"}:
                raise NotImplementedError(
                    "Only $regex/$options query operators are supported"
                )
            options = value.get("$options", "")
            if not isinstance(options, str) or set(options) - set("imsx"):
                raise ValueError("Supported regex options are i, m, s, x")
            pattern = value["$regex"]
            if not isinstance(pattern, str):
                raise TypeError("$regex must be a string")
            pattern = f"(?{options}){pattern}" if options else pattern
            re.compile(pattern)  # Report invalid patterns before SQLite executes them.
            clauses.append(
                f"json_type(document, {path}) = 'text' AND {expression} REGEXP ?"
            )
            parameters.append(pattern)
            continue
        if isinstance(value, datetime):
            value = value.isoformat()
        if isinstance(value, (dict, list)):
            kind = "object" if isinstance(value, dict) else "array"
            value = _pack({"value": value})[0]
            value = json.dumps(json.loads(value)["value"], separators=(",", ":"))
        elif isinstance(value, bool):
            kind = "true" if value else "false"
        elif isinstance(value, str):
            kind = "text"
        elif value is None or isinstance(value, (int, float)):
            kind = None
            if value is not None:
                clauses.append(f"json_type(document, {path}) IN ('integer', 'real')")
        else:
            raise TypeError(f"Unsupported filter value: {type(value).__name__}")
        if kind:
            clauses.append(f"json_type(document, {path}) = ?")
            parameters.append(kind)
        clauses.append(f"{expression} IS ?")
        parameters.append(value)
    return (" AND ".join(clauses) or "1"), parameters


def _project(document: dict, projection: Optional[dict]) -> dict:
    """Apply the include/exclude projections used by database helpers."""
    if not projection:
        return document
    if not isinstance(projection, dict):
        raise TypeError("A projection must be a dictionary")
    for field, value in projection.items():
        if not isinstance(field, str) or "." in field or value not in (0, 1):
            raise NotImplementedError(
                "Only top-level include/exclude projections are supported"
            )
    included = {key for key, value in projection.items() if value and key != "_id"}
    excluded = {key for key, value in projection.items() if not value and key != "_id"}
    if included and excluded:
        raise ValueError("Cannot mix inclusion and exclusion projections")
    if included or (projection.get("_id") and not excluded):
        keys = included | ({"_id"} if projection.get("_id", 1) else set())
        return {key: value for key, value in document.items() if key in keys}
    return {key: value for key, value in document.items() if projection.get(key, 1)}


class Database:
    """Store collections in one SQLite file with indexed ID lookups."""

    def __init__(self, path: Union[str, Path]) -> None:
        if str(path) != ":memory:":
            Path(path).expanduser().parent.mkdir(parents=True, exist_ok=True)
            path = str(Path(path).expanduser())
        self._lock = RLock()
        self._connection = sqlite3.connect(path, timeout=30, check_same_thread=False)
        self._connection.create_function(
            "regexp",
            2,
            lambda pattern, value: isinstance(value, str)
            and re.search(pattern, value) is not None,
        )
        # WAL allows readers during writes; SQLite transactions protect counters
        # even when another process opens the same file.
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.executescript("""
            CREATE TABLE IF NOT EXISTS documents (
                row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                collection TEXT NOT NULL,
                document TEXT NOT NULL,
                dates TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS collection_idx ON documents(collection);
            CREATE UNIQUE INDEX IF NOT EXISTS document_id_idx
                ON documents(collection, json_extract(document, '$._id'));
            """)
        for field in ("chat_id", "user_id", "unique_id", "key"):
            self._connection.execute(
                f"CREATE INDEX IF NOT EXISTS {field}_idx ON documents"
                f"(collection, json_extract(document, '$.{field}'))"
            )
        self._connection.commit()

    def __getitem__(self, name: str) -> "Collection":
        """Keep database()["collection"] access unchanged."""
        if not isinstance(name, str) or not name:
            raise ValueError("A collection name must be a non-empty string")
        return Collection(self, name)

    @contextmanager
    def _transaction(self):
        """Serialize read/modify/write operations across threads and processes."""
        with self._lock, self._connection:
            self._connection.execute("BEGIN IMMEDIATE")
            yield

    def close(self) -> None:
        """Release the connection (primarily for maintenance tools and tests)."""
        with self._lock:
            self._connection.close()

    def import_documents(self, collections: dict) -> int:
        """Import an export atomically, refusing to merge into occupied collections."""
        count = 0
        with self._transaction():
            for name, documents in collections.items():
                collection = self[name]
                if collection._select(None, 1):
                    raise ValueError(f"Collection {name!r} already contains data")
                for document in documents:
                    collection._insert(document)
                    count += 1
        return count


class Collection:
    """Implement the synchronous collection operations used by the bot."""

    def __init__(self, database: Database, name: str) -> None:
        self._database = database
        self.name = name

    def _select(self, query: Optional[dict], limit: Optional[int] = None) -> list:
        clause, parameters = _where(query)
        sql = (
            "SELECT row_id, document, dates FROM documents "
            f"WHERE collection = ? AND ({clause}) ORDER BY row_id"
        )
        if limit is not None:
            sql += " LIMIT ?"
            parameters.append(limit)
        with self._database._lock:
            return self._database._connection.execute(
                sql, [self.name] + parameters
            ).fetchall()

    def find(
        self, filter: Optional[dict] = None, projection: Optional[dict] = None
    ) -> Iterator[dict]:
        """Return an iterable snapshot in insertion order, as profiles expect."""
        rows = self._select(filter)
        return (_project(_unpack(data, dates), projection) for _, data, dates in rows)

    def find_one(
        self, filter: Optional[dict] = None, projection: Optional[dict] = None
    ) -> Optional[dict]:
        """Return the first match or None."""
        rows = self._select(filter, 1)
        return _project(_unpack(*rows[0][1:]), projection) if rows else None

    def _insert(self, document: dict) -> Any:
        document.setdefault("_id", uuid4().hex)
        data, dates = _pack(document)
        self._database._connection.execute(
            "INSERT INTO documents(collection, document, dates) VALUES (?, ?, ?)",
            (self.name, data, dates),
        )
        return document["_id"]

    def insert_one(self, document: dict) -> InsertOneResult:
        """Insert a document, assigning an _id just like the previous driver."""
        with self._database._transaction():
            return InsertOneResult(self._insert(document))

    def _update(self, query: dict, update: dict, upsert: bool) -> tuple:
        if not isinstance(update, dict) or not update:
            raise ValueError("An update requires $set, $inc, or $unset")
        for operator, values in update.items():
            if operator not in {"$set", "$inc", "$unset"}:
                raise NotImplementedError(f"Unsupported update operator: {operator}")
            if not isinstance(values, dict):
                raise TypeError("Update operator values must be dictionaries")
            for key, value in values.items():
                if key == "_id" or "." in key or key.startswith("$"):
                    raise ValueError("Updates require top-level fields other than _id")
                if operator == "$inc" and (
                    isinstance(value, bool) or not isinstance(value, (int, float))
                ):
                    raise TypeError("$inc requires numeric values")
        rows = self._select(query, 1)
        if not rows and not upsert:
            return UpdateResult(0, 0), None, None
        before = _unpack(*rows[0][1:]) if rows else None
        after = (
            deepcopy(before)
            if before is not None
            else {
                key: value
                for key, value in query.items()
                if not isinstance(value, dict)
            }
        )
        for operator, values in update.items():
            for key, value in values.items():
                if operator == "$set":
                    after[key] = value
                elif operator == "$unset":
                    after.pop(key, None)
                else:
                    current = after.get(key, 0)
                    if isinstance(current, bool) or not isinstance(
                        current, (int, float)
                    ):
                        raise TypeError("$inc cannot update a non-numeric field")
                    after[key] = current + value
        if rows:
            data, dates = _pack(after)
            self._database._connection.execute(
                "UPDATE documents SET document = ?, dates = ? WHERE row_id = ?",
                (data, dates, rows[0][0]),
            )
            result = UpdateResult(1, int((data, dates) != rows[0][1:]))
        else:
            result = UpdateResult(0, 0, self._insert(after))
        return result, before, after

    def update_one(
        self, filter: dict, update: dict, upsert: bool = False
    ) -> UpdateResult:
        """Atomically update the first match, optionally inserting when missing."""
        with self._database._transaction():
            return self._update(filter, update, upsert)[0]

    def find_one_and_update(
        self,
        filter: dict,
        update: dict,
        projection: Optional[dict] = None,
        return_document: bool = False,
        upsert: bool = False,
    ) -> Optional[dict]:
        """Return the document before the update, or after when requested."""
        with self._database._transaction():
            _, before, after = self._update(filter, update, upsert)
            document = after if return_document else before
            return _project(document, projection) if document is not None else None

    def _delete(self, query: dict, limit: Optional[int]) -> DeleteResult:
        with self._database._transaction():
            rows = self._select(query, limit)
            self._database._connection.executemany(
                "DELETE FROM documents WHERE row_id = ?", [(row[0],) for row in rows]
            )
            return DeleteResult(len(rows))

    def delete_one(self, filter: dict) -> DeleteResult:
        """Delete only the first matching document."""
        return self._delete(filter, 1)

    def delete_many(self, filter: dict) -> DeleteResult:
        """Delete all matches, leaving other chats and collections untouched."""
        return self._delete(filter, None)
