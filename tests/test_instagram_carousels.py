"""Offline regression checks for Instagram carousel downloads and uploads."""

import logging
import sys
import types
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from pyrogram.errors import BadRequest
from test_social_downloader import ROOT, load_module


class CarouselTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        package = types.ModuleType("userbot")
        package.LOGS = logging.getLogger(__name__)
        with patch.dict(sys.modules, {"userbot": package}):
            self.instagram = load_module("carousel_instagram", ROOT / "userbot/helpers/instagram.py")
        self.upload = load_module("carousel_upload", ROOT / "userbot/helpers/social_upload.py")

    async def test_current_extractor_downloads_music_post_as_original_photo(self):
        """Use current media metadata and omit background audio by default."""
        media = {
            "media_type": 1,
            "image_versions2": {
                "candidates": [
                    {
                        "width": 100,
                        "height": 100,
                        "url": "https://example.com/small.jpg",
                    },
                    {
                        "width": 1080,
                        "height": 1350,
                        "url": "https://example.com/original.jpg",
                    },
                ]
            },
            "music_metadata": {
                "music_info": {
                    "music_asset_info": {
                        "progressive_download_url": "https://example.com/song.m4a",
                    }
                }
            },
        }

        def extract(extractor, url):
            return extractor._extract_product(media, video_id="ABC", get_comments=False)

        client = MagicMock()
        with (
            patch.object(self.instagram, "YoutubeDL", return_value=client),
            patch.object(
                self.instagram.InstagramIE,
                "extract",
                autospec=True,
                side_effect=extract,
            ),
            patch.object(self.instagram, "_download_asset") as download,
            patch.object(self.instagram, "render_photo", new=AsyncMock()) as render,
        ):
            result = await self.instagram.download_instagram_photo(
                "https://www.instagram.com/p/ABC/", "tmp", None, "agent"
            )
        self.assertEqual(result["media_type"], "photo")
        self.assertEqual(result["file_path"], "tmp/instagram-photo.jpg")
        download.assert_called_once_with(
            client.__enter__.return_value,
            "https://example.com/original.jpg",
            "tmp/instagram-photo.jpg",
        )
        render.assert_not_awaited()

    async def test_current_extractor_rejects_video_thumbnails(self):
        """A failed video must never be reported as its cover photo."""
        client = MagicMock()
        extractor = self.instagram._InstagramPhotoIE(client)
        with patch.object(
            self.instagram.InstagramIE, "_extract_product", return_value={}
        ):
            extractor._extract_product(
                {
                    "media_type": 2,
                    "video_versions": [{"url": "https://example.com/video.mp4"}],
                    "image_versions2": {
                        "candidates": [{"url": "https://example.com/cover.jpg"}]
                    },
                }
            )
        self.assertIsNone(extractor.photo_metadata)

    async def test_metadata_and_download_result(self):
        photos = [{"media_type": 1, "display_url": f"https://example.com/{i}.jpg"} for i in range(3)]
        for media in (
            {"carousel_media": photos},
            {"edge_sidecar_to_children": {"edges": [{"node": p} for p in photos]}},
        ):
            details = self.instagram.photo_post_details(media)
            self.assertEqual([p["image_url"] for p in details["photos"]], [p["display_url"] for p in photos])
        for children in ([], photos + [{"is_video": True}], photos * 7):
            self.assertIsNone(self.instagram.photo_post_details({"carousel_media": children}))
        with patch.object(self.instagram, "_fetch_photo", return_value={
            "image_paths": ["1.jpg", "2.jpg"], "title": "Album"
        }):
            result = await self.instagram.download_instagram_photo("url", "tmp", None, "agent")
        self.assertEqual(result["media_type"], "photos")
        self.assertEqual(result["file_paths"], ["1.jpg", "2.jpg"])

    async def test_batches_captions_and_replies(self):
        for count, sizes in ((1, []), (10, [10]), (11, [10]), (20, [10, 10])):
            bot = types.SimpleNamespace(send_media_group=AsyncMock(), send_photo=AsyncMock())
            paths = [f"{i}.jpg" for i in range(count)]
            await self.upload.send_photos(bot, 123, 42, paths, "caption")
            albums = [c.args[1] for c in bot.send_media_group.await_args_list]
            singles = bot.send_photo.await_args_list
            self.assertEqual([len(a) for a in albums], sizes)
            self.assertEqual([p.media for a in albums for p in a] + [c.args[1] for c in singles], paths)
            self.assertEqual([p.caption for a in albums for p in a] + [c.kwargs["caption"] for c in singles],
                             ["caption"] + [""] * (count - 1))
            for call in bot.send_media_group.await_args_list + singles:
                self.assertEqual(call.kwargs["reply_parameters"].message_id, 42)

    async def test_rejected_album_and_photos_use_documents(self):
        bot = types.SimpleNamespace(
            send_media_group=AsyncMock(side_effect=BadRequest("rejected")),
            send_photo=AsyncMock(side_effect=BadRequest("rejected")),
            send_document=AsyncMock(),
        )
        await self.upload.send_photos(bot, 123, None, ["1.jpg", "2.jpg"], "caption")
        calls = bot.send_document.await_args_list
        self.assertEqual([c.args[1] for c in calls], ["1.jpg", "2.jpg"])
        self.assertEqual([c.kwargs["caption"] for c in calls], ["caption", ""])
        self.assertIsNone(calls[0].kwargs["reply_parameters"])
