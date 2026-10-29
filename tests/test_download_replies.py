"""Exercise reply routing through the outgoing download handler and fallbacks."""

import logging
import sys
import types
import unittest
from unittest.mock import AsyncMock, patch

from pyrogram.errors import BadRequest
from test_social_downloader import ROOT, load_module


class DownloadReplyTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        package = types.ModuleType("userbot")
        package.LOGS = logging.getLogger(__name__)
        package.SOCKS5_PROXY = None
        package.UserBot = types.SimpleNamespace(on_message=lambda *a, **k: lambda f: f)
        instagram = types.ModuleType("userbot.helpers.instagram")
        instagram.run_process = AsyncMock(return_value=(1, b"", b"ERROR: unavailable"))
        instagram.download_instagram_photo = AsyncMock()
        downloader = types.ModuleType("userbot.helpers.social_downloader")
        downloader.prepare_telegram_video = AsyncMock()
        help_module = types.ModuleType("userbot.plugins.help")
        help_module.add_command_help = lambda *a: None
        upload = load_module("reply_upload", ROOT / "userbot/helpers/social_upload.py")
        with patch.dict(sys.modules, {
            "userbot": package,
            "userbot.helpers.instagram": instagram,
            "userbot.helpers.social_downloader": downloader,
            "userbot.helpers.social_upload": upload,
            "userbot.plugins.help": help_module,
        }):
            self.module = load_module("reply_video", ROOT / "userbot/plugins/video_dl.py")
        self.module.process_urls = AsyncMock(side_effect=lambda url: url)
        self.source = types.SimpleNamespace(
            id=42, chat=types.SimpleNamespace(id=123), reply_to_message_id=None,
            text="https://instagram.com/p/ABC/", caption=None, delete=AsyncMock(),
        )
        self.status = types.SimpleNamespace(id=99, edit=AsyncMock(), delete=AsyncMock())
        self.bot = types.SimpleNamespace(
            send_message=AsyncMock(return_value=self.status),
            send_video=AsyncMock(), send_photo=AsyncMock(),
            send_media_group=AsyncMock(), send_document=AsyncMock(),
        )

    async def check_upload(self, kind, fallback=False, command=False, reply_to=None):
        """Every attempted upload must reply to the retained source link."""
        self.source.reply_to_message_id = reply_to
        self.module.download_instagram_photo.return_value = {
            "media_type": kind, "file_path": "media.mp4", "title": "Title",
            "file_paths": ["one.jpg", "two.jpg"], "fallback_image_path": "cover.jpg",
        }
        if fallback:
            self.bot.send_video.side_effect = BadRequest("rejected")
            self.bot.send_media_group.side_effect = BadRequest("rejected")
            self.bot.send_photo.side_effect = BadRequest("rejected")
        if command:
            trigger = types.SimpleNamespace(reply_to_message=self.source, delete=AsyncMock())
            await self.module.download_video_command(self.bot, trigger)
            trigger.delete.assert_awaited_once()
        else:
            await self.module.video_downloader(self.bot, self.source)
        uploads = [call for method in (self.bot.send_video, self.bot.send_photo,
                   self.bot.send_media_group, self.bot.send_document)
                   for call in method.await_args_list]
        self.assertTrue(uploads)
        for call in uploads:
            self.assertEqual(call.args[0], 123)
            self.assertEqual(
                call.kwargs["reply_parameters"].message_id,
                reply_to if reply_to and not command else 42,
            )
        self.source.delete.assert_not_awaited()
        self.status.delete.assert_awaited_once()
        if fallback:
            self.bot.send_document.assert_awaited()

    async def test_automatic_video(self):
        await self.check_upload("video")

    async def test_automatic_photo(self):
        await self.check_upload("photo")

    async def test_automatic_album(self):
        await self.check_upload("photos")

    async def test_video_to_photo_to_document(self):
        await self.check_upload("video", fallback=True)

    async def test_album_to_photos_to_documents(self):
        await self.check_upload("photos", fallback=True)

    async def test_explicit_command_replies_to_source(self):
        await self.check_upload("video", command=True)

    async def test_link_reply_inherits_target_for_all_media_and_fallbacks(self):
        for kind, fallback in (("video", False), ("photo", False),
                               ("photos", False), ("video", True),
                               ("photo", True), ("photos", True)):
            with self.subTest(kind=kind, fallback=fallback):
                self.setUp()
                await self.check_upload(kind, fallback=fallback, reply_to=17)

    async def test_explicit_command_keeps_target_when_link_is_reply(self):
        await self.check_upload("video", command=True, reply_to=17)
