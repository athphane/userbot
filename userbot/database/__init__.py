"""Shared local database, retaining the collection API used by the helpers."""

from functools import lru_cache

from userbot import DB_PATH
from userbot.database.sqlite import Database


@lru_cache(maxsize=1)
def database() -> Database:
    """Open the configured SQLite file once per process."""
    return Database(DB_PATH)
