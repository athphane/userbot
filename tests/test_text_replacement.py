"""Check automatic Twitter/X link cleanup without connecting to Telegram."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch


class TwitterLinkTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        """Load the plugin with client setup and help registration stubbed out."""
        package = types.ModuleType("userbot")
        package.UserBot = types.SimpleNamespace(on_message=lambda *a, **k: lambda f: f)
        help_module = types.ModuleType("userbot.plugins.help")
        help_module.add_command_help = lambda *a: None
        path = Path(__file__).resolve().parents[1] / "userbot/plugins/text_replacement.py"
        spec = importlib.util.spec_from_file_location("text_replacement_test", path)
        self.plugin = importlib.util.module_from_spec(spec)
        with patch.dict(
            sys.modules,
            {"userbot": package, "userbot.plugins.help": help_module},
        ):
            spec.loader.exec_module(self.plugin)

    async def test_shared_link_is_cleaned_and_keeps_preview(self) -> None:
        """The example copied from X must produce a query-free FxTwitter link."""
        message = types.SimpleNamespace(
            text="https://x.com/youhatefive/status/2115847903696527589?a=zUqsO08gc89VXFj7cHA&s=19",
            edit=AsyncMock(),
        )
        await self.plugin.twitter_url_fixer(None, message)
        message.edit.assert_awaited_once()
        self.assertEqual(
            message.edit.await_args.args[0],
            "https://fxtwitter.com/youhatefive/status/2115847903696527589",
        )
        self.assertTrue(
            message.edit.await_args.kwargs["link_preview_options"].show_above_text
        )

    async def test_hosts_paths_and_surrounding_text(self) -> None:
        """Clean every supported URL while preserving other links and punctuation."""
        cases = [
            (
                f"https://{host}/user/status/123/video/1?s=19&t=tracking",
                "https://fxtwitter.com/user/status/123/video/1",
            )
            for host in (
                "twitter.com",
                "x.com",
                "www.twitter.com",
                "www.x.com",
                "mobile.twitter.com",
                "X.COM",
            )
        ]
        cases.extend(
            [
                ("http://twitter.com/user", "http://fxtwitter.com/user"),
                (
                    "See (https://x.com/user/status/123?s=19), then "
                    "https://twitter.com/other/status/456?t=abc.\n"
                    "https://example.com/?s=19",
                    "See (https://fxtwitter.com/user/status/123), then "
                    "https://fxtwitter.com/other/status/456.\n"
                    "https://example.com/?s=19",
                ),
                (
                    "https://x.com/user/status/123?s=19#section",
                    "https://fxtwitter.com/user/status/123#section",
                ),
                (
                    "https://x.com.example.com/user/status/123?s=19",
                    "https://x.com.example.com/user/status/123?s=19",
                ),
            ]
        )
        for original, expected in cases:
            with self.subTest(text=original):
                message = types.SimpleNamespace(text=original, edit=AsyncMock())
                await self.plugin.twitter_url_fixer(None, message)
                self.assertEqual(message.edit.await_args.args[0], expected)
