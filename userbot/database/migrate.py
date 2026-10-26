"""Import mongoexport JSON without requiring MongoDB or Telegram dependencies.

Run directly: python userbot/database/migrate.py exports --database config/userbot.sqlite3
"""

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

if __package__:
    from .sqlite import Database
else:
    from sqlite import Database


def _extended_json(value: dict):
    """Decode the Extended JSON types present in this bot's MongoDB documents."""
    if set(value) == {"$oid"}:
        return value["$oid"]
    if set(value) == {"$date"}:
        date = value["$date"]
        if isinstance(date, (int, float)):
            return datetime.fromtimestamp(date / 1000, timezone.utc).replace(
                tzinfo=None
            )
        parsed = datetime.fromisoformat(date.replace("Z", "+00:00"))
        if parsed.tzinfo is not None:
            parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    for tag, convert in (
        ("$numberInt", int),
        ("$numberLong", int),
        ("$numberDouble", float),
    ):
        if set(value) == {tag}:
            return convert(value[tag])
    if any(key.startswith("$") for key in value):
        raise ValueError(f"Unsupported Extended JSON object: {list(value)}")
    return value


def read_exports(directory: Path) -> dict:
    """Read collection-named JSON arrays or newline-delimited mongoexport files."""
    files = sorted(directory.glob("*.json"))
    if not files:
        raise ValueError("No collection JSON files found in the export directory")
    collections = {}
    for path in files:
        text = path.read_text(encoding="utf-8").strip()
        if text.startswith("["):
            documents = json.loads(text, object_hook=_extended_json)
        else:
            documents = [
                json.loads(line, object_hook=_extended_json)
                for line in text.splitlines()
                if line.strip()
            ]
        if not isinstance(documents, list) or not all(
            isinstance(doc, dict) for doc in documents
        ):
            raise ValueError(f"{path.name} must contain JSON documents")
        collections[path.stem] = documents
    return collections


def main() -> None:
    """Import into an explicit SQLite file without loading userbot configuration."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "exports", type=Path, help="Directory of collection-name.json files"
    )
    parser.add_argument(
        "--database", default="config/userbot.sqlite3", help="Destination SQLite file"
    )
    args = parser.parse_args()
    try:
        collections = read_exports(args.exports)
        database = Database(args.database)
        try:
            count = database.import_documents(collections)
        finally:
            database.close()
    except (OSError, ValueError, TypeError, OverflowError, sqlite3.Error) as error:
        parser.exit(1, f"Import failed: {error}\n")
    print(
        f"Imported {count} documents from {len(collections)} collections into {args.database}"
    )


if __name__ == "__main__":
    main()
