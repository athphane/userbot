"""Check dictionary lookups and Telegram formatting without a Telegram login."""

import importlib.util
import sys
import types
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
from pyrogram.enums import ParseMode


class DictionaryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        """Load the plugin without client setup or help registration."""
        package = types.ModuleType("userbot")
        package.UserBot = types.SimpleNamespace(on_message=lambda *a, **k: lambda f: f)
        help_module = types.ModuleType("userbot.plugins.help")
        help_module.add_command_help = lambda *a: None
        path = Path(__file__).resolve().parents[1] / "userbot/plugins/dictionary.py"
        spec = importlib.util.spec_from_file_location("dictionary_test", path)
        self.plugin = importlib.util.module_from_spec(spec)
        with patch.dict(
            sys.modules, {"userbot": package, "userbot.plugins.help": help_module}
        ):
            spec.loader.exec_module(self.plugin)

    @staticmethod
    def response() -> dict:
        """Use the documented response shape, including both attribution fields."""
        return {
            "word": "hello",
            "entries": [
                {
                    "partOfSpeech": "interjection",
                    "pronunciations": [{"type": "ipa", "text": "/həˈloʊ/"}],
                    "senses": [
                        {"definition": "A <greeting> & welcome.", "examples": ["Hi!"]}
                    ],
                    "synonyms": ["hi", "hey"],
                    "antonyms": ["goodbye"],
                }
            ],
            "source": {"url": "https://en.wiktionary.org/wiki/hello"},
        }

    def test_rendering_and_empty_results(self) -> None:
        """Render the API fields as escaped HTML with visible source credits."""
        output = self.plugin.format_entries(self.response())
        root = ET.fromstring(f"<root>{output}</root>")
        self.assertIn("A &lt;greeting&gt; &amp; welcome.", output)
        self.assertIn("/həˈloʊ/", output)
        self.assertIn("hi, hey", output)
        self.assertIn("goodbye", output)
        self.assertEqual(
            [link.text for link in root.findall("a")],
            ["FreeDictionaryAPI.com", "Wiktionary"],
        )
        self.assertEqual(self.plugin.format_entries({"entries": []}), "")

    def test_long_fields_remain_valid_bounded_html(self) -> None:
        """Long multiline fields cannot split tags, entities, or emoji pairs."""
        for field in ("word", "ipa", "definition", "example", "synonym"):
            with self.subTest(field=field):
                data = self.response()
                entry = data["entries"][0]
                text = "<&😀\n" * 3000
                if field == "word":
                    data["word"] = text
                elif field == "ipa":
                    entry["pronunciations"][0]["text"] = text
                elif field == "definition":
                    entry["senses"][0]["definition"] = text
                elif field == "example":
                    entry["senses"][0]["examples"] = [text]
                else:
                    entry["synonyms"] = [text]
                output = self.plugin.format_entries(data)
                root = ET.fromstring(f"<root>{output}</root>")
                self.assertLessEqual(len(output.encode("utf-16-le")) // 2, 4096)
                self.assertIn("…", output)
                self.assertEqual(root.findall("a")[-1].text, "Wiktionary")

    async def test_fetch_encodes_word_and_bounds_request_time(self) -> None:
        """Encode a word as one path segment and check HTTP status before JSON."""
        response = MagicMock()
        response.json = AsyncMock(return_value=self.response())
        session = MagicMock()
        session.get.return_value.__aenter__.return_value = response
        with patch.object(self.plugin.aiohttp, "ClientSession") as client_session:
            client_session.return_value.__aenter__.return_value = session
            self.assertEqual(await self.plugin.fetch_entries("a/b ?#"), self.response())
        self.assertEqual(client_session.call_args.kwargs["timeout"].total, 10)
        session.get.assert_called_once_with(
            "https://freedictionaryapi.com/api/v1/entries/en/a%2Fb%20%3F%23"
        )
        response.raise_for_status.assert_called_once_with()

    async def test_lookup_errors_are_reported(self) -> None:
        """HTTP, timeout, and malformed JSON errors must produce a useful reply."""
        for error in (aiohttp.ClientError("offline"), TimeoutError(), ValueError()):
            with self.subTest(error=type(error).__name__):
                message = types.SimpleNamespace(
                    command=["dict", "hello"], edit=AsyncMock()
                )
                with patch.object(self.plugin, "fetch_entries", side_effect=error):
                    await self.plugin.define(None, message)
                self.assertIn("unreachable", message.edit.await_args.args[0])

    async def test_reply_lookup_and_missing_word(self) -> None:
        """Use replied text and display not-found results as escaped HTML."""
        message = types.SimpleNamespace(
            command=["dict"],
            reply_to_message=types.SimpleNamespace(text=" <missing> "),
            edit=AsyncMock(),
        )
        with patch.object(
            self.plugin, "fetch_entries", return_value={"entries": []}
        ) as fetch:
            await self.plugin.define(None, message)
        fetch.assert_awaited_once_with("<missing>")
        self.assertIn("&lt;missing&gt;", message.edit.await_args.args[0])
        self.assertEqual(message.edit.await_args.kwargs["parse_mode"], ParseMode.HTML)

    async def test_successful_lookup_disables_link_previews(self) -> None:
        """Use Kurigram's current options when displaying an attributed result."""
        message = types.SimpleNamespace(command=["dict", "hello"], edit=AsyncMock())
        with patch.object(self.plugin, "fetch_entries", return_value=self.response()):
            await self.plugin.define(None, message)
        options = message.edit.await_args.kwargs
        self.assertEqual(options["parse_mode"], ParseMode.HTML)
        self.assertTrue(options["link_preview_options"].is_disabled)
