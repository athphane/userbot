"""Persistence and helper behavior checks using real SQLite, without Telegram."""

import importlib
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import textwrap
import types
import unittest
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_store():
    """Load the store without importing the configured Telegram application."""
    spec = importlib.util.spec_from_file_location(
        "sqlite_store_test", ROOT / "userbot/database/sqlite.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


store = load_store()


class SQLiteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name, "nested", "userbot.sqlite3")
        self.db = store.Database(self.path)
        self.addCleanup(self.db.close)
        self.collection = self.db["records"]

    def test_persistence_types_and_collection_isolation(self) -> None:
        """Signed Telegram IDs, dates, Unicode, and JSON must survive reopening."""
        date = datetime(2026, 10, 25, 12, 1, 2, 345678)
        document = {
            "chat_id": -1001234567890,
            "user_id": 9007199254740991,
            "ignored": True,
            "empty": None,
            "last_message_time": date,
            "nested": {"dates": [date.replace(tzinfo=timezone.utc)]},
            "text": "Reminder: café 🐈 ' \\ \n",
        }
        result = self.collection.insert_one(document)
        self.assertEqual(result.inserted_id, document["_id"])
        other = store.Database(self.path)
        self.addCleanup(other.close)
        self.assertEqual(
            other["records"].find_one({"chat_id": document["chat_id"]}), document
        )
        self.assertIsNone(other["other"].find_one())
        self.assertEqual(
            list(other["records"].find({}, {"user_id": 1, "_id": 0})),
            [{"user_id": document["user_id"]}],
        )
        self.assertEqual(
            other["records"].find_one({}, {"_id": 1}), {"_id": result.inserted_id}
        )
        self.assertNotIn("_id", other["records"].find_one({}, {"_id": 0}))

    def test_filters_and_projection_do_not_leak_other_chats(self) -> None:
        for chat_id, sticker_id in ((1, "one"), (1, "two"), (2, "one")):
            self.collection.insert_one({"chat_id": chat_id, "sticker_id": sticker_id})
        self.assertEqual(
            list(self.collection.find({"chat_id": 1, "sticker_id": "two"}, {"_id": 0})),
            [{"chat_id": 1, "sticker_id": "two"}],
        )
        self.assertEqual(self.collection.delete_one({"chat_id": 1}).deleted_count, 1)
        self.assertEqual(self.collection.delete_many({"chat_id": 1}).deleted_count, 1)
        self.assertEqual(self.collection.find_one()["chat_id"], 2)
        self.assertEqual(self.collection.delete_one({"chat_id": 99}).deleted_count, 0)

    def test_scalar_types_and_null_matching(self) -> None:
        for value in (True, False, 1, 0, "1", None):
            self.collection.insert_one({"value": value})
        self.collection.insert_one({"missing": True})
        for value in (True, False, 1, 0, "1"):
            with self.subTest(value=value):
                matches = list(self.collection.find({"value": value}))
                self.assertEqual(len(matches), 1)
                self.assertIs(type(matches[0]["value"]), type(value))
        self.assertEqual(len(list(self.collection.find({"value": None}))), 2)

    def test_queries_are_parameterized(self) -> None:
        text = "x' OR 1=1; DROP TABLE documents; --"
        collection = self.db[text]
        collection.insert_one({"content": text})
        self.assertEqual(collection.find_one({"content": text})["content"], text)
        self.assertIsNone(self.collection.find_one({"content": text}))
        self.assertIsNone(collection.find_one({"content": "other"}))

    def test_regex_search_matches_strings_only(self) -> None:
        for content in ("Buy Milk", "milkshake", "coffee", None, 123):
            self.collection.insert_one({"content": content})
        matches = list(
            self.collection.find(
                {"content": {"$regex": "^buy milk$", "$options": "i"}},
                {"content": 1, "_id": 0},
            )
        )
        self.assertEqual(matches, [{"content": "Buy Milk"}])
        self.assertEqual(
            len(list(self.collection.find({"content": {"$regex": "milk"}}))), 1
        )

    def test_updates_and_returned_documents(self) -> None:
        self.collection.insert_one({"user_id": 1, "score": 2, "remove": True})
        result = self.collection.update_one(
            {"user_id": 1}, {"$inc": {"score": 1, "new": 1}, "$unset": {"remove": ""}}
        )
        self.assertEqual((result.matched_count, result.modified_count), (1, 1))
        before = self.collection.find_one_and_update(
            {"user_id": 1}, {"$set": {"score": 4}}
        )
        after = self.collection.find_one_and_update(
            {"user_id": 1}, {"$inc": {"score": 1}}, return_document=True
        )
        self.assertEqual((before["score"], after["score"]), (3, 5))
        self.assertNotIn("remove", after)
        result = self.collection.update_one({"user_id": 1}, {"$set": {"score": 5}})
        self.assertEqual((result.matched_count, result.modified_count), (1, 0))
        result = self.collection.update_one({"user_id": 999}, {"$set": {"score": 1}})
        self.assertEqual((result.matched_count, result.modified_count), (0, 0))
        self.assertIsNone(self.collection.find_one({"user_id": 999}))

    def test_upsert_updates_one_existing_setting(self) -> None:
        first = self.collection.update_one(
            {"key": "pm_permit"}, {"$set": {"value": True}}, upsert=True
        )
        second = self.collection.update_one(
            {"key": "pm_permit"}, {"$set": {"value": False}}, upsert=True
        )
        self.assertIsNotNone(first.upserted_id)
        self.assertIsNone(second.upserted_id)
        self.assertEqual(
            list(self.collection.find({}, {"_id": 0})),
            [{"key": "pm_permit", "value": False}],
        )

    def test_concurrent_counters_across_connections(self) -> None:
        """Read/modify/write must hold a SQLite write transaction, not only a thread lock."""
        self.collection.insert_one({"user_id": 1, "score": 0})
        second = store.Database(self.path)
        self.addCleanup(second.close)
        collections = [self.collection, second["records"]]

        def increment(index):
            collections[index % 2].update_one({"user_id": 1}, {"$inc": {"score": 1}})

        with ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(increment, range(100)))
        self.assertEqual(self.collection.find_one({"user_id": 1})["score"], 100)

    def test_failed_update_rolls_back_and_connection_remains_usable(self) -> None:
        self.collection.insert_one({"user_id": 1, "text": "original"})
        with self.assertRaises(TypeError):
            self.collection.update_one(
                {"user_id": 1}, {"$set": {"text": "changed"}, "$inc": {"text": 1}}
            )
        self.assertEqual(self.collection.find_one()["text"], "original")
        self.collection.update_one({"user_id": 1}, {"$set": {"text": "next"}})
        self.assertEqual(self.collection.find_one()["text"], "next")

    def test_unsupported_operators_fail_without_modifying_data(self) -> None:
        self.collection.insert_one({"user_id": 1})
        with self.assertRaises(NotImplementedError):
            self.collection.delete_many({"user_id": {"$unknown": 1}})
        with self.assertRaises(NotImplementedError):
            self.collection.update_one({}, {"$push": {"values": 1}})
        with self.assertRaises(ValueError):
            self.collection.update_one({}, {"$set": {"_id": "replacement"}})
        self.assertEqual(len(list(self.collection.find())), 1)

    def test_import_is_atomic_and_refuses_existing_data(self) -> None:
        self.collection.insert_one({"_id": "id"})
        with self.assertRaises(ValueError):
            self.db.import_documents({"new": [{"a": 1}], "records": [{"a": 2}]})
        self.assertIsNone(self.db["new"].find_one())
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.import_documents(
                {"new": [{"_id": "duplicate"}, {"_id": "duplicate"}]}
            )
        self.assertIsNone(self.db["new"].find_one())


class DatabaseHelperTests(unittest.TestCase):
    def setUp(self) -> None:
        """Keep the public database factory and all helper implementations real."""
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        package = types.ModuleType("userbot")
        package.__path__ = [str(ROOT / "userbot")]
        package.DB_PATH = str(Path(self.directory.name, "userbot.sqlite3"))
        # Isolate package modules, including eager ignore_db construction.
        modules = {
            name: module
            for name, module in sys.modules.items()
            if name == "userbot" or name.startswith("userbot.")
        }
        for name in modules:
            del sys.modules[name]
        sys.modules["userbot"] = package

        def restore():
            for name in list(sys.modules):
                if name == "userbot" or name.startswith("userbot."):
                    del sys.modules[name]
            sys.modules.update(modules)

        self.addCleanup(restore)
        self.database = importlib.import_module("userbot.database").database
        self.addCleanup(self.database().close)

    def helper(self, module: str, name: str):
        return getattr(importlib.import_module(f"userbot.database.{module}"), name)()

    @staticmethod
    def message(chat_id: int, sticker: str = "sticker"):
        return types.SimpleNamespace(
            chat=types.SimpleNamespace(id=chat_id),
            from_user=types.SimpleNamespace(id=1),
            sticker=types.SimpleNamespace(file_unique_id=sticker),
        )

    def test_stickers_auto_replies_and_summon(self) -> None:
        message = self.message(-100123)
        for module, name in (
            ("sticker_deleter", "StickerDeleter"),
            ("auto_replies", "AutoReplies"),
        ):
            helper = self.helper(module, name)
            helper.add_sticker_in_chat(message)
            helper.add_sticker_in_chat(self.message(-100123, "second"))
            helper.add_sticker_in_chat(self.message(-100999))
            self.assertIsNotNone(helper.find_chat_id(message))
            self.assertEqual(list(helper.get_chat_ids())[0], {"chat_id": -100123})
            self.assertTrue(helper.delete_sticker_in_chat(message))
            self.assertIsNone(helper.find_chat_id(message))
            self.assertIsNotNone(helper.find_chat_id(self.message(-100999)))
            self.assertFalse(helper.delete_sticker_in_chat(message))
        summon = self.helper("summon", "SUMMON")
        summon.add_chat_id(message)
        summon.update(message, 123.5, 18000)
        self.assertEqual(summon.find_chat_id(message)["last_send"], 123.5)
        self.assertTrue(summon.delete_chat_id(message))
        self.assertFalse(summon.delete_chat_id(message))
        self.assertIs(self.database(), self.database())

    def test_ignore_timestamp_is_a_datetime(self) -> None:
        ignore = importlib.import_module("userbot.database.ignore").ignore_db
        ignore.ignore_user(123)
        self.assertTrue(ignore.is_ignored(123))
        self.assertIsNone(ignore.get_last_message_time(123))
        ignore.set_last_message_time(123)
        date = ignore.get_last_message_time(123)
        self.assertIsInstance(date, datetime)
        self.assertLess((datetime.now() - date).total_seconds(), 5)
        ignore.unignore_user(123)
        self.assertFalse(ignore.is_ignored(123))

    def test_pmpermit_approval_warnings_counters_and_blocking(self) -> None:
        permit = self.helper("pmpermit", "PmPermit")
        self.assertFalse(permit.check_if_approved(1))
        self.assertFalse(permit.check_if_warned(1))
        self.assertTrue(permit.warn(1))
        self.assertFalse(permit.warn(1))
        for _ in range(3):
            permit.increment_retard_level(1)
        self.assertEqual(permit.calculate_retard_level(1), 3)
        self.assertTrue(permit.approve(1))
        self.assertTrue(permit.check_if_approved(1))
        self.assertFalse(permit.approve(1))
        self.assertTrue(permit.block_pm(1))
        self.assertTrue(permit.check_if_force_blocked(1))

    def test_reminders_profiles_and_settings(self) -> None:
        reminders = self.helper("reminders", "Reminders")
        reminders.add_reminder("Buy milk 🥛")
        unique_id, content = reminders.get_all_reminders()[0]
        self.assertEqual(content, "Buy milk 🥛")
        self.assertEqual(reminders.find_reminder(unique_id)["content"], content)
        reminders.delete_reminder(unique_id)
        self.assertEqual(reminders.get_all_reminders(), [])
        profiles = self.helper("profiles", "Profiles")
        profiles.add_profile(1, "One", "one")
        profiles.add_profile(2, "Two", "two")
        self.assertEqual(profiles.getProfile(2)["title"], "Two")
        self.assertEqual(
            [profile["channel_id"] for profile in profiles.all_profiles()], [1, 2]
        )
        settings = self.helper("settings", "Settings")
        settings.set_pm_permit(True)
        settings.set_pm_permit(False)
        self.assertEqual(
            list(self.database()["settings"].find({}, {"_id": 0})),
            [{"key": "pm_permit", "value": False}],
        )


class MigrationAndStartupTests(unittest.TestCase):
    def test_standalone_import_without_application_dependencies(self) -> None:
        """The migration CLI must work even with site packages disabled."""
        with tempfile.TemporaryDirectory() as directory:
            exports = Path(directory, "exports")
            exports.mkdir()
            date = {"$date": {"$numberLong": "1767225600000"}}
            Path(exports, "ignored_users.json").write_text(
                json.dumps(
                    [
                        {
                            "_id": {"$oid": "abcdef"},
                            "user_id": {"$numberLong": "123"},
                            "ignored": True,
                            "last_message_time": date,
                        }
                    ]
                )
            )
            Path(exports, "self_reminders.json").write_text(
                json.dumps({"unique_id": "first", "content": "milk"})
                + "\n"
                + json.dumps({"unique_id": "second", "content": "coffee"})
                + "\n"
            )
            path = Path(directory, "userbot.sqlite3")
            command = [
                sys.executable,
                "-S",
                str(ROOT / "userbot/database/migrate.py"),
                str(exports),
                "--database",
                str(path),
            ]
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            db = store.Database(path)
            try:
                self.assertEqual(
                    db["ignored_users"].find_one()["last_message_time"],
                    datetime(2026, 1, 1),
                )
                self.assertEqual(db["ignored_users"].find_one()["user_id"], 123)
                self.assertEqual(len(list(db["self_reminders"].find())), 2)
                repeat = subprocess.run(
                    command, capture_output=True, text=True, timeout=30
                )
                self.assertNotEqual(repeat.returncode, 0)
                self.assertEqual(len(list(db["self_reminders"].find())), 2)
            finally:
                db.close()

    def test_bootstrap_needs_no_mongo_configuration_or_driver(self) -> None:
        for legacy in (False, True):
            with self.subTest(
                legacy_config=legacy
            ), tempfile.TemporaryDirectory() as directory:
                config = ConfigParser()
                config.read(ROOT / "userbot.ini.sample")
                config.remove_section("database")
                if legacy:
                    config["mongo"] = {"url": "unused.invalid", "db_name": "legacy"}
                Path(directory, "config").mkdir()
                with Path(directory, "config/userbot.ini").open("w") as output:
                    config.write(output)
                script = textwrap.dedent("""
                    import asyncio
                    import sys

                    async def check():
                        from userbot.database import database
                        db = database()
                        db["test"].insert_one({"key": "value"})
                        assert db["test"].find_one()["key"] == "value"
                        assert not any(
                            name == "pymongo" or name.startswith("pymongo.")
                            for name in sys.modules
                        )
                        db.close()

                    asyncio.run(check())
                """)
                result = subprocess.run(
                    [sys.executable, "-c", script],
                    cwd=directory,
                    env={**os.environ, "PYTHONPATH": str(ROOT)},
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(Path(directory, "config/userbot.sqlite3").is_file())


if __name__ == "__main__":
    unittest.main()
