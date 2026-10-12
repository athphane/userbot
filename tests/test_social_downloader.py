"""Offline checks for the social downloader port."""

import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    """Load a helper without starting the configured Telegram client."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class URLTests(unittest.TestCase):
    def setUp(self):
        package = types.ModuleType("userbot")
        package.__path__ = []
        helpers = types.ModuleType("userbot.helpers")
        helpers.__path__ = []
        instagram = types.ModuleType("userbot.helpers.instagram")
        instagram.download_instagram_photo = AsyncMock()
        instagram.run_process = AsyncMock()
        self.modules = patch.dict(sys.modules, {
            "userbot": package, "userbot.helpers": helpers,
            "userbot.helpers.instagram": instagram,
        })
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.downloader = load_module(
            "social_downloader_test", ROOT / "userbot/helpers/social_downloader.py"
        )

    def test_auto_platforms_exclude_long_youtube_and_facebook(self):
        cases = [
            ("https://vm.tiktok.com/abc/", "TikTok"),
            ("https://ddinstagram.com/reel/ABC", "Instagram"),
            ("https://youtube.com/shorts/ABC", "YouTube Shorts"),
        ]
        for url, expected in cases:
            with self.subTest(url=url):
                self.assertEqual(self.downloader.detect_platform(f"see {url}", True)[0], expected)
        for url in ("https://youtu.be/ABC", "https://facebook.com/reel/123"):
            with self.subTest(url=url):
                self.assertIsNone(self.downloader.detect_platform(url, True)[0])
                self.assertIsNotNone(self.downloader.detect_platform(url)[0])

    def test_first_supported_link_is_chosen(self):
        text = "https://youtube.com/shorts/one then https://instagram.com/reel/two"
        name, match = self.downloader.detect_platform(text)
        self.assertEqual(name, "YouTube Shorts")
        self.assertEqual(match.group(0), "https://youtube.com/shorts/one")

    def test_final_yt_dlp_error_survives_long_warning(self):
        stderr = b"WARNING: " + b"x" * 600 + b"\nERROR: Video unavailable"
        self.assertEqual(self.downloader.download_error(stderr, "YouTube"), "Video unavailable")


class DownloadTests(unittest.IsolatedAsyncioTestCase):
    async def test_youtube_calls_conversion(self):
        package = types.ModuleType("userbot")
        package.__path__ = []
        helpers = types.ModuleType("userbot.helpers")
        helpers.__path__ = []
        instagram = types.ModuleType("userbot.helpers.instagram")
        instagram.download_instagram_photo = AsyncMock()
        instagram.run_process = AsyncMock(return_value=(0, b"", b""))
        with patch.dict(sys.modules, {
            "userbot": package, "userbot.helpers": helpers,
            "userbot.helpers.instagram": instagram,
        }):
            module = load_module(
                "social_downloader_download_test", ROOT / "userbot/helpers/social_downloader.py"
            )
            with tempfile.TemporaryDirectory() as directory:
                Path(directory, "Short [ABC].webm").write_bytes(b"video")
                converted = str(Path(directory, "telegram.mp4"))
                with patch.object(module, "prepare_telegram_video", new=AsyncMock(return_value=converted)) as convert:
                    result = await module.download_video("https://youtube.com/shorts/ABC", directory)
                self.assertEqual(result["title"], "Short")
                self.assertEqual(result["file_path"], converted)
                convert.assert_awaited_once()
                args = instagram.run_process.await_args.args
                self.assertIn("--no-playlist", args)


class AccessTests(unittest.IsolatedAsyncioTestCase):
    async def test_allowlist_and_group_membership(self):
        access = load_module("social_access_test", ROOT / "userbot/helpers/social_access.py")
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(access, "ALLOWLIST_PATH", str(Path(directory, "allowlist.json"))):
                self.assertTrue(access.add_user(123))
                self.assertFalse(access.add_user(123))
                self.assertEqual(access.list_users(), [123])
                self.assertEqual(json.loads(Path(access.ALLOWLIST_PATH).read_text()), {"allowed_users": [123]})
                bot = types.SimpleNamespace(get_chat_member=AsyncMock(return_value=types.SimpleNamespace(status="member")))
                self.assertTrue(await access.is_user_allowed(bot, 123, 1, -100))
                self.assertTrue(await access.is_user_allowed(bot, 456, 1, -100))
                bot.get_chat_member.return_value.status = "left"
                self.assertFalse(await access.is_user_allowed(bot, 456, 1, -100))
                self.assertTrue(access.remove_user(123))
                self.assertFalse(access.remove_user(123))
