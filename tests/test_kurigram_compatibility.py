"""Exercise the real Kurigram client, plugins, and SQLite without Telegram."""

import asyncio
import importlib.util
import logging
import os
import sqlite3
import sys
import tempfile
import types
import unittest
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

from pyrogram import enums
from pyrogram.types import Chat, ChatMember, ChatPhoto, Message, User

ROOT = Path(__file__).resolve().parents[1]


class KurigramTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        """Load all plugins with a disconnected client and a real SQLite database."""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        previous = os.getcwd()
        self.addCleanup(os.chdir, previous)
        Path(directory.name, "userbot").symlink_to(
            ROOT / "userbot", target_is_directory=True
        )
        os.chdir(directory.name)

        spec = importlib.util.spec_from_file_location(
            "migration_client", ROOT / "userbot/userbot.py"
        )
        core = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(core)
        config = ConfigParser()
        config.read_dict({"pyrogram": {"api_id": "1", "api_hash": "0" * 32}})
        with patch.object(core, "ConfigParser", return_value=config):
            self.client = core.UserBot()

        self.package = types.ModuleType("userbot")
        self.package.__path__ = [str(ROOT / "userbot")]
        for name, value in {
            "UserBot": self.client,
            "ALLOWED_USERS": [1],
            "CMD_HELP": {},
            "START_TIME": datetime.now(),
            "LOGS": logging.getLogger("migration-test"),
            "SOCKS5_PROXY": None,
            "SPOTIFY_CLIENT_ID": None,
            "SPOTIFY_CLIENT_SECRET": None,
            "SPOTIFY_USERNAME": None,
            "YOURLS_URL": None,
            "YOURLS_KEY": None,
            "DB_PATH": ":memory:",
        }.items():
            setattr(self.package, name, value)
        previous_modules = {
            name: module
            for name, module in sys.modules.items()
            if name == "userbot" or name.startswith("userbot.")
        }
        self.restore_modules({"userbot": self.package})
        self.addCleanup(self.restore_modules, previous_modules)
        from userbot.database import database

        self.addCleanup(database().close)
        self.client.load_plugins()
        await asyncio.sleep(0)

    @staticmethod
    def restore_modules(modules: dict) -> None:
        """Isolate bot globals while keeping third-party process resources alive."""
        for name in list(sys.modules):
            if name == "userbot" or name.startswith("userbot."):
                del sys.modules[name]
        sys.modules.update(modules)

    def message(self, command: str) -> Message:
        """Build a command message bound to the actual disconnected client."""
        message = Message(
            client=self.client,
            id=10,
            chat=Chat(id=-100123, type=enums.ChatType.SUPERGROUP),
            from_user=User(id=1, first_name="Owner", is_self=True),
            text=f".{command}",
        )
        message.command = command.split()
        return message

    async def test_all_plugins_register_handlers(self) -> None:
        """Every plugin must import and register with Kurigram's dispatcher."""
        modules = {
            handler.callback.__module__
            for group in self.client.dispatcher.groups.values()
            for handler in group
        }
        for path in (ROOT / "userbot/plugins").rglob("*.py"):
            name = ".".join(path.relative_to(ROOT).with_suffix("").parts)
            with self.subTest(plugin=name):
                self.assertIn(name, modules)
        self.assertIn("start", self.package.CMD_HELP)

    async def test_client_lifecycle_forwards_kurigram_options(self) -> None:
        """The subclass must accept the keyword arguments used by Client.run."""
        from pyrogram import Client

        async def history(*args, **kwargs):
            if False:
                yield None

        with (
            patch.object(Client, "start", new=AsyncMock()) as start,
            patch.object(Client, "stop", new=AsyncMock()) as stop,
            patch.object(Client, "search_messages", history),
            patch.object(
                self.client,
                "get_me",
                new=AsyncMock(return_value=types.SimpleNamespace(username="test")),
            ),
        ):
            self.assertIs(
                await self.client.start(use_qr=True, except_ids=[1]), self.client
            )
            start.assert_awaited_once_with(use_qr=True, except_ids=[1])
            self.assertIs(
                await self.client.stop(block=False, clear_handlers=False), self.client
            )
            stop.assert_awaited_once_with(block=False, clear_handlers=False)

    async def test_admin_checks_use_member_status_and_privileges(self) -> None:
        """Owners may restrict users; administrators need the explicit right."""
        helper = sys.modules["userbot.helpers.adminHelpers"]
        message = self.message("ban")
        from pyrogram.types import ChatAdministratorRights

        cases = [
            (ChatMember(status=enums.ChatMemberStatus.OWNER), True),
            (
                ChatMember(
                    status=enums.ChatMemberStatus.ADMINISTRATOR,
                    privileges=ChatAdministratorRights(can_restrict_members=True),
                ),
                True,
            ),
            (
                ChatMember(
                    status=enums.ChatMemberStatus.ADMINISTRATOR,
                    privileges=ChatAdministratorRights(can_restrict_members=False),
                ),
                False,
            ),
            (ChatMember(status=enums.ChatMemberStatus.MEMBER), False),
        ]
        for member, expected in cases:
            with (
                self.subTest(status=member.status, allowed=expected),
                patch.object(
                    self.client,
                    "get_chat_member",
                    new_callable=AsyncMock,
                    return_value=member,
                ),
                patch.object(self.client, "edit_message_text", new_callable=AsyncMock),
                patch.object(self.client, "delete_messages", new_callable=AsyncMock),
                patch.object(helper.asyncio, "sleep", new=AsyncMock()),
            ):
                self.assertEqual(await helper.CheckAdmin(message), expected)

    async def test_timed_ban_passes_a_datetime(self) -> None:
        """Timed restrictions must not silently become permanent bans."""
        plugin = sys.modules["userbot.plugins.admin.administrator"]
        message = self.message("ban 2")
        message.reply_to_message = Message(
            id=9, from_user=User(id=2, first_name="Member")
        )
        with (
            patch.object(plugin, "CheckAdmin", new=AsyncMock(return_value=True)),
            patch.object(self.client, "ban_chat_member", new_callable=AsyncMock) as ban,
            patch.object(self.client, "edit_message_text", new_callable=AsyncMock),
        ):
            await plugin.ban_hammer(self.client, message)
        until = ban.call_args.kwargs["until_date"]
        self.assertIsInstance(until, datetime)
        self.assertAlmostEqual((until - datetime.now()).total_seconds(), 7200, delta=5)

    async def test_profile_uses_chat_photos_and_datetime_status(self) -> None:
        """Profile inspection must consume the photo iterator and its new fields."""
        plugin = sys.modules["userbot.plugins.whois"]
        date = datetime(2026, 10, 25, 12)
        user = User(
            id=2,
            first_name="Member",
            status=enums.UserStatus.OFFLINE,
            last_online_date=date,
        )
        photo = ChatPhoto(
            small_file_id="small",
            small_photo_unique_id="small-id",
            big_file_id="large",
            big_photo_unique_id="large-id",
            added_date=date,
        )

        async def photos(*args, **kwargs):
            yield photo

        with (
            patch.object(
                self.client, "get_users", new_callable=AsyncMock, return_value=user
            ),
            patch.object(
                self.client,
                "get_chat",
                new_callable=AsyncMock,
                return_value=types.SimpleNamespace(bio="Bio"),
            ),
            patch.object(self.client, "get_chat_photos", photos),
            patch.object(
                self.client,
                "get_chat_photos_count",
                new_callable=AsyncMock,
                return_value=1,
            ),
            patch.object(
                self.client, "get_common_chats", new_callable=AsyncMock, return_value=[]
            ),
            patch.object(self.client, "send_photo", new_callable=AsyncMock) as send,
            patch.object(self.client, "delete_messages", new_callable=AsyncMock),
        ):
            await plugin.who_is(self.client, self.message("whois 2"))
        self.assertEqual(send.call_args.args[1], "large")
        self.assertIn("25.10.2026, 12:00:00", send.call_args.kwargs["caption"])
        self.assertIn("Sun, 25 Oct 2026", send.call_args.kwargs["caption"])

    async def test_music_uses_the_returned_inline_message(self) -> None:
        """Inline sends return a Message rather than raw Updates."""
        plugin = sys.modules["userbot.plugins.music"]
        result = types.SimpleNamespace(
            query_id=42, results=[types.SimpleNamespace(id="song")]
        )
        saved = Message(id=50, audio=types.SimpleNamespace(file_id="audio"))
        message = self.message("music song")
        message.reply_to_message = Message(id=9)
        with (
            patch.object(
                self.client,
                "get_inline_bot_results",
                new_callable=AsyncMock,
                return_value=result,
            ),
            patch.object(
                self.client,
                "send_inline_bot_result",
                new_callable=AsyncMock,
                return_value=saved,
            ),
            patch.object(self.client, "send_audio", new_callable=AsyncMock) as send,
            patch.object(self.client, "delete_messages", new_callable=AsyncMock),
        ):
            await plugin.send_music(self.client, message)
        send.assert_awaited_once()
        self.assertEqual(send.call_args.kwargs["audio"], "audio")
        self.assertEqual(send.call_args.kwargs["reply_parameters"].message_id, 9)

    async def test_lyrics_copy_the_returned_inline_message(self) -> None:
        """Lyrics must copy and remove the Message returned by Kurigram."""
        plugin = sys.modules["userbot.plugins.lyrics"]
        result = types.SimpleNamespace(
            query_id=42, results=[types.SimpleNamespace(id="lyrics")]
        )
        with (
            patch.object(
                self.client,
                "get_inline_bot_results",
                new_callable=AsyncMock,
                return_value=result,
            ),
            patch.object(
                self.client,
                "send_inline_bot_result",
                new_callable=AsyncMock,
                return_value=Message(id=50),
            ),
            patch.object(self.client, "copy_message", new_callable=AsyncMock) as copy,
            patch.object(
                self.client, "delete_messages", new_callable=AsyncMock
            ) as delete,
            patch.object(self.client, "edit_message_text", new_callable=AsyncMock),
            patch.object(plugin.asyncio, "sleep", new=AsyncMock()),
        ):
            await plugin.send_lyrics(self.client, self.message("lyrics song"))
        self.assertEqual(copy.call_args.kwargs["message_id"], 50)
        self.assertIn(unittest.mock.call("me", 50), delete.call_args_list)

    async def test_stickers_keep_replies_and_omit_inline_attribution(self) -> None:
        """Re-send the sticker file because Kurigram removed hide_via."""
        plugin = sys.modules["userbot.plugins.memes.stickers"]
        result = types.SimpleNamespace(
            query_id=42, results=[types.SimpleNamespace(id="sticker")]
        )
        saved = Message(id=50, sticker=types.SimpleNamespace(file_id="sticker-file"))
        message = self.message("mock text")
        message.reply_to_message = Message(id=9)
        with (
            patch.object(
                self.client,
                "get_inline_bot_results",
                new_callable=AsyncMock,
                return_value=result,
            ),
            patch.object(
                self.client,
                "send_inline_bot_result",
                new_callable=AsyncMock,
                return_value=saved,
            ) as inline,
            patch.object(self.client, "send_sticker", new_callable=AsyncMock) as send,
            patch.object(self.client, "delete_messages", new_callable=AsyncMock),
            patch.object(self.client, "edit_message_text", new_callable=AsyncMock),
        ):
            await plugin.sticker_super_func(self.client, message)
        self.assertEqual(inline.call_args.kwargs["chat_id"], "me")
        self.assertEqual(send.call_args.kwargs["sticker"], "sticker-file")
        self.assertEqual(send.call_args.kwargs["reply_parameters"].message_id, 9)

    async def test_message_edits_use_link_preview_options(self) -> None:
        """Bound Message.edit rejects the old disable_web_page_preview argument."""
        plugin = sys.modules["userbot.plugins.text_replacement"]
        message = self.message("r/python")
        with patch.object(
            self.client, "edit_message_text", new_callable=AsyncMock
        ) as edit:
            await plugin.subreddit_link(self.client, message)
        self.assertTrue(edit.call_args.kwargs["link_preview_options"].is_disabled)


class SessionMigrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_existing_session_retains_authorization_and_peer_cache(self) -> None:
        """Upgrade a synthetic pyrotgfork session using Kurigram's built-in migration."""
        from pyrogram.storage.sqlite_storage import SQLiteStorage

        with tempfile.TemporaryDirectory() as directory:
            auth_key = bytes(range(256))
            with sqlite3.connect(Path(directory, "legacy.session")) as connection:
                connection.executescript(
                    (ROOT / "tests/fixtures/pyrotgfork_v6.sql").read_text()
                )
                connection.execute("INSERT INTO version VALUES (6)")
                connection.execute(
                    "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (2, 123, 0, auth_key, 0, 456, 0),
                )
                connection.execute(
                    "INSERT INTO peers (id, access_hash, type) VALUES (789, 42, 'user')"
                )
                connection.execute("INSERT INTO usernames VALUES (789, 'member')")
                connection.execute(
                    "INSERT INTO update_state VALUES (0, 10, 20, 30, 40)"
                )

            storage = SQLiteStorage("legacy", Path(directory))
            await storage.open()
            try:
                self.assertEqual(await storage.version(), storage.VERSION)
                self.assertEqual(await storage.api_id(), 123)
                self.assertEqual(await storage.user_id(), 456)
                self.assertEqual(await storage.auth_key(), auth_key)
                self.assertEqual(await storage.server_address(), "149.154.167.51")
                self.assertEqual(await storage.port(), 443)
                peer = await storage.get_peer_by_id(789)
                self.assertEqual(peer.user_id, 789)
                self.assertEqual(peer.access_hash, 42)
                self.assertEqual(
                    storage.conn.execute("SELECT username FROM usernames").fetchone()[
                        0
                    ],
                    "member",
                )
                self.assertEqual(
                    storage.conn.execute(
                        "SELECT pts FROM update_state WHERE id = 0"
                    ).fetchone()[0],
                    10,
                )
            finally:
                await storage.close()


if __name__ == "__main__":
    unittest.main()
