"""Offline regression checks for dependencies used by the bot's helpers."""

import asyncio
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import textwrap
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from PIL import Image
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[1]


def load_helper(name: str):
    """Load a helper without starting the configured Telegram client."""
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "userbot" / "helpers" / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TelegramDependencyTests(unittest.TestCase):
    def test_client_event_loop_and_native_crypto_without_connecting(self) -> None:
        """Check Kurigram and TgCrypto-pyrofork without a Telegram login."""
        script = textwrap.dedent("""
            import asyncio

            import tgcrypto
            from pyrogram import Client

            async def check_loop():
                client = Client("compatibility", api_id=1, api_hash="0" * 32, in_memory=True)
                assert asyncio.get_running_loop() is client.loop

            asyncio.run(check_loop())

            data, key, iv = bytes(32), bytes(range(32)), bytes(32)
            encrypted = tgcrypto.ige256_encrypt(data, key, iv)
            assert encrypted != data
            assert tgcrypto.ige256_decrypt(encrypted, key, iv) == data
            """)
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class ImageTests(unittest.TestCase):
    def test_skyrim_images_render_with_current_pillow(self):
        """Both short and wide text must render after the font API migration."""
        helper = load_helper("skyrim")
        for text in ("Sneak", "An unusually long achievement name"):
            with self.subTest(text=text), tempfile.TemporaryDirectory() as directory:
                with patch.object(helper.SkyrimStatusMeme, "finalSize", [300, 200]):
                    meme = helper.SkyrimStatusMeme(text, "100")
                    output = Path(directory) / "meme.png"
                    meme.SaveFile(output)
                    with Image.open(output) as image:
                        image.load()
                        self.assertEqual(image.height, 200)
                        self.assertGreater(image.width, meme.GetSize()[0])

    def test_svg_conversion_with_current_lxml(self):
        """The contribution-graph SVG parser must still build a drawing."""
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"><rect width="20" height="20" fill="green"/></svg>'
        drawing = svg2rlg(io.BytesIO(svg))
        self.assertIsNotNone(drawing)
        self.assertEqual((drawing.width, drawing.height), (15, 15))
        png = renderPM.drawToString(drawing, fmt="PNG", dpi=96)
        with Image.open(io.BytesIO(png)) as image:
            self.assertEqual(image.size, (20, 20))
            self.assertEqual(image.convert("RGB").getpixel((10, 10)), (0, 128, 0))


class StartupTests(unittest.IsolatedAsyncioTestCase):
    async def test_client_and_scheduler_share_the_running_loop(self) -> None:
        """Kurigram and scheduled jobs must share the entry point's loop."""
        scheduler = AsyncIOScheduler()
        completed = asyncio.Event()

        async def job() -> None:
            completed.set()

        scheduler.add_job(job, "date")
        package = types.ModuleType("userbot")
        package.UserBot = types.SimpleNamespace(start=AsyncMock(), stop=AsyncMock())
        package.scheduler = scheduler
        spec = importlib.util.spec_from_file_location(
            "entrypoint", ROOT / "userbot" / "__main__.py"
        )
        entrypoint = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(entrypoint)

        async def idle() -> None:
            package.UserBot.start.assert_awaited_once()
            self.assertTrue(scheduler.running)
            await asyncio.wait_for(completed.wait(), timeout=5)

        with patch.dict(sys.modules, {"userbot": package}), patch.object(
            entrypoint, "idle", idle
        ):
            await entrypoint.main()
        self.assertIs(package.client, package.UserBot)
        self.assertFalse(scheduler.running)
        package.UserBot.stop.assert_awaited_once()


class AsyncDependencyTests(unittest.IsolatedAsyncioTestCase):
    async def test_scheduler_runs_jobs_without_pkg_resources(self):
        """Exercise scheduler plugin loading with patched setuptools."""
        completed = asyncio.Event()

        async def job() -> None:
            completed.set()

        scheduler = AsyncIOScheduler()
        scheduler.add_job(job, "date")
        scheduler.start()
        try:
            await asyncio.wait_for(completed.wait(), timeout=5)
        finally:
            scheduler.shutdown()
            await asyncio.sleep(0)

    async def test_tiktok_helper_uses_yt_dlp(self):
        """The legacy helper retains its output path after replacing youtube-dl."""
        helper = load_helper("tiktokHelper")
        with tempfile.TemporaryDirectory() as directory:
            previous = os.getcwd()
            try:
                os.chdir(directory)
                Path("downloads").mkdir()
                Path("downloads/downloaded_file.mp4").write_bytes(b"video")
                with patch.object(helper, "YoutubeDL") as downloader:
                    result = await helper.TikTok.download_tiktok(
                        "https://example.com/video"
                    )
                downloader.return_value.__enter__.return_value.download.assert_called_once_with(
                    ["https://example.com/video"]
                )
                self.assertEqual(result, "downloads/downloaded_file.mp4")
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
