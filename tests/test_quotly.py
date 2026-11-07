"""Check QuotLyBot quoting and status messages without a Telegram login."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from pyrogram.parser.markdown import Markdown


class QuotlyTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        """Load the plugin without client setup or help registration."""
        package = types.ModuleType("userbot")
        package.UserBot = types.SimpleNamespace(on_message=lambda *a, **k: lambda f: f)
        help_module = types.ModuleType("userbot.plugins.help")
        help_module.add_command_help = lambda *a: None
        path = Path(__file__).resolve().parents[1] / "userbot/plugins/quotly.py"
        spec = importlib.util.spec_from_file_location("quotly_test", path)
        self.plugin = importlib.util.module_from_spec(spec)
        with patch.dict(
            sys.modules, {"userbot": package, "userbot.plugins.help": help_module}
        ):
            spec.loader.exec_module(self.plugin)

    @staticmethod
    def message() -> types.SimpleNamespace:
        """Reply to a text message whose forward to QuotLyBot gets id 50."""
        return types.SimpleNamespace(
            chat=types.SimpleNamespace(id=-100123),
            reply_to_message=types.SimpleNamespace(
                forward=AsyncMock(return_value=types.SimpleNamespace(id=50))
            ),
            edit=AsyncMock(),
            delete=AsyncMock(),
        )

    @staticmethod
    def bot(*polls: types.SimpleNamespace) -> types.SimpleNamespace:
        """Return one QuotLyBot history item per poll, repeating the last one."""
        remaining = list(polls)

        async def history(*args, **kwargs):
            yield remaining.pop(0) if len(remaining) > 1 else remaining[0]

        return types.SimpleNamespace(
            get_chat_history=history, forward_messages=AsyncMock()
        )

    async def run_quotly(self, bot, message) -> None:
        """Run the handler without waiting between polls."""
        with patch.object(self.plugin.asyncio, "sleep", new=AsyncMock()):
            await self.plugin.quotly(bot, message)

    async def test_status_edits_are_never_empty(self) -> None:
        """Single-line ``` blocks parse to MESSAGE_EMPTY, so every edit needs text."""
        message = self.message()
        await self.run_quotly(self.bot(types.SimpleNamespace(id=50, sticker=None)), message)
        # Initial status, one progress edit per poll, then the timeout notice.
        self.assertEqual(message.edit.await_count, self.plugin.MAX_POLLS + 2)
        for call in message.edit.await_args_list:
            with self.subTest(text=call.args[0]):
                parsed = await Markdown(None).parse(call.args[0])
                self.assertTrue(parsed["message"])

    async def test_forwards_only_a_sticker_newer_than_the_quoted_message(self) -> None:
        """An older quote sticker in the bot chat must not be sent back."""
        message = self.message()
        bot = self.bot(
            types.SimpleNamespace(id=49, sticker=object()),
            types.SimpleNamespace(id=51, sticker=object()),
        )
        await self.run_quotly(bot, message)
        message.reply_to_message.forward.assert_awaited_once_with("@QuotLyBot")
        bot.forward_messages.assert_awaited_once_with(-100123, "@QuotLyBot", 51)
        message.delete.assert_awaited_once_with()

    async def test_unanswered_quote_stops_with_a_timeout(self) -> None:
        """Stop polling when QuotLyBot never replies instead of looping forever."""
        message = self.message()
        bot = self.bot(types.SimpleNamespace(id=50, sticker=None))
        await self.run_quotly(bot, message)
        bot.forward_messages.assert_not_awaited()
        self.assertIn("did not respond", message.edit.await_args.args[0])

    async def test_missing_reply_is_reported(self) -> None:
        """Ask for a reply instead of forwarding anything."""
        message = types.SimpleNamespace(reply_to_message=None, edit=AsyncMock())
        await self.plugin.quotly(None, message)
        self.assertIn("Reply", message.edit.await_args.args[0])
