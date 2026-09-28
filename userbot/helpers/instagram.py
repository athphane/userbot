"""Best-effort support for Instagram still photos with music."""

import asyncio
import json
import math
import os
import re
import time
from urllib.parse import urlencode

from yt_dlp import YoutubeDL
from yt_dlp.networking import Request

from userbot import LOGS

MAX_ASSET_SIZE = 50 * 1024 * 1024


async def run_process(*args: str, timeout: float = 300) -> tuple[int, bytes, bytes]:
    """Reap subprocesses on timeout/cancellation before their files are removed."""
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout)
        return process.returncode, stdout, stderr
    finally:
        if process.returncode is None:
            try:
                process.kill()
            except ProcessLookupError:
                pass
            await process.communicate()


def _number(value: object, default: float = 0) -> float:
    """Coerce metadata timing and dimensions to finite, nonnegative numbers."""
    try:
        value = float(value)
        return value if math.isfinite(value) and value >= 0 else default
    except (TypeError, ValueError):
        return default


def photo_details(media: dict) -> dict | None:
    """Only accept actual single photos, never a failed video's thumbnail."""
    if (
        media.get("is_video")
        or media.get("video_url")
        or media.get("video_versions")
        or media.get("carousel_media")
        or media.get("edge_sidecar_to_children")
    ):
        return None
    if not (
        media.get("media_type") == 1
        or media.get("is_video") is False
        or media.get("__typename") in ("GraphImage", "XDTGraphImage")
    ):
        return None
    candidates = (media.get("image_versions2") or {}).get("candidates") or []
    candidates = sorted(
        candidates,
        key=lambda c: _number(c.get("width")) * _number(c.get("height")),
        reverse=True,
    )
    image_url = next(
        (c.get("url") for c in candidates if c.get("url")), None
    ) or media.get("display_url")
    if not image_url:
        return None

    music = media.get("music_metadata") or media.get("clips_metadata") or {}
    info = music.get("music_info") or {}
    asset = info.get("music_asset_info") or {}
    consumption = info.get("music_consumption_info") or {}
    original = music.get("original_sound_info") or {}
    audio_url = asset.get("progressive_download_url") or original.get(
        "progressive_download_url"
    )
    # Photo posts can expose music directly in clips_music_attribution_info.
    attribution = media.get("clips_music_attribution_info") or {}
    audio_url = audio_url or attribution.get("progressive_download_url")
    start_ms = consumption.get("start_time_in_ms")
    if start_ms is None:
        starts = consumption.get("overlap_start_times") or []
        start_ms = starts[0] if starts else 0
    duration_ms = consumption.get("duration_in_ms")
    duration = _number(duration_ms) / 1000 or _number(media.get("video_duration")) or 15
    caption = media.get("caption") or {}
    title = caption.get("text") if isinstance(caption, dict) else caption
    if not title:
        edges = (media.get("edge_media_to_caption") or {}).get("edges") or []
        title = (edges[0].get("node") or {}).get("text") if edges else None
    return {
        "image_url": image_url,
        "audio_url": audio_url,
        "start": _number(start_ms) / 1000,
        "duration": min(duration, 90),
        "title": title or "Instagram photo",
    }


def _download_asset(client: YoutubeDL, url: str, path: str) -> None:
    """Download one asset with bounded size and duration."""
    if not isinstance(url, str) or not url.startswith("https://"):
        raise ValueError("Invalid Instagram asset URL")
    deadline = time.monotonic() + 120
    with client.urlopen(Request(url)) as response, open(path, "wb") as output:
        size = 0
        while chunk := response.read(64 * 1024):
            size += len(chunk)
            if size > MAX_ASSET_SIZE or time.monotonic() > deadline:
                raise ValueError("Instagram asset exceeds download limits")
            output.write(chunk)
    if not size:
        raise ValueError("Empty Instagram asset")


def _fetch_photo(
    url: str, temp_dir: str, proxy: str | None, user_agent: str
) -> dict | None:
    """Fetch verified single-photo metadata and its image and optional audio."""
    match = re.search(r"instagram\.com/(?:p|reels?|tv)/([\w-]+)", url)
    if not match:
        return None
    shortcode = match.group(1)
    headers = {
        "User-Agent": user_agent,
        "Referer": url,
        "X-IG-App-ID": "936619743392459",
    }
    with YoutubeDL(
        {
            "quiet": True,
            "proxy": proxy or "",
            "socket_timeout": 20,
            "http_headers": headers,
        }
    ) as client:
        # The web-info query retains photo music metadata. Keep the legacy query
        # as a fallback for posts served through the older response shape.
        details = None
        for doc_id in ("27128499623469141", "8845758582119845"):
            query = urlencode(
                {
                    "doc_id": doc_id,
                    "variables": json.dumps(
                        {
                            "shortcode": shortcode,
                            "__relay_internal__pv__PolarisAIGMMediaWebLabelEnabledrelayprovider": False,
                        }
                    ),
                }
            )
            try:
                with client.urlopen(
                    Request("https://www.instagram.com/graphql/query/?" + query)
                ) as response:
                    data = json.loads(response.read(8 * 1024 * 1024))["data"]
                items = (data.get("xdt_api__v1__media__shortcode__web_info") or {}).get(
                    "items"
                ) or []
                media = items[0] if items else data.get("xdt_shortcode_media") or {}
                details = photo_details(media)
                if details:
                    break
            except Exception:
                LOGS.debug("Instagram photo metadata query failed", exc_info=True)
        if not details:
            return None
        image_path = os.path.join(temp_dir, "instagram-photo.jpg")
        _download_asset(client, details["image_url"], image_path)
        details["image_path"] = image_path
        if details["audio_url"]:
            try:
                audio_path = os.path.join(temp_dir, "instagram-audio.m4a")
                _download_asset(client, details["audio_url"], audio_path)
                details["audio_path"] = audio_path
            except Exception:
                LOGS.info("Instagram audio unavailable; using photo", exc_info=True)
        return details


async def render_photo(
    image_path: str,
    audio_path: str,
    output_path: str,
    start: float = 0,
    duration: float = 15,
) -> None:
    """Render a still image with its music clip into a Telegram-compatible video."""
    code, _, _ = await run_process(
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-nostdin",
        "-y",
        "-loop",
        "1",
        "-framerate",
        "30",
        "-i",
        image_path,
        "-ss",
        str(start),
        "-i",
        audio_path,
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-vf",
        "scale=w='min(1080,iw)':h='min(1920,ih)':force_original_aspect_ratio=decrease,pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-c:v",
        "libx264",
        "-tune",
        "stillimage",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-t",
        str(duration),
        "-shortest",
        "-movflags",
        "+faststart",
        output_path,
        timeout=180,
    )
    if code or not os.path.exists(output_path) or not os.path.getsize(output_path):
        raise ValueError("Photo video rendering failed")
    # A seek beyond available audio can produce a container without audio.
    code, stdout, _ = await run_process(
        "ffprobe",
        "-v",
        "error",
        "-show_streams",
        "-of",
        "json",
        output_path,
        timeout=15,
    )
    streams = json.loads(stdout).get("streams", []) if code == 0 else []
    if not {"audio", "video"} <= {s.get("codec_type") for s in streams}:
        raise ValueError("Rendered video is missing audio or video")


async def download_instagram_photo(
    url: str, temp_dir: str, proxy: str | None, user_agent: str
) -> dict | None:
    """Download a photo, rendering music when available with an image fallback."""
    # Shield the worker so cancellation cannot race with temp-directory cleanup.
    worker = asyncio.create_task(
        asyncio.to_thread(_fetch_photo, url, temp_dir, proxy, user_agent)
    )
    try:
        details = await asyncio.shield(worker)
    except asyncio.CancelledError:
        await worker
        raise
    if not details:
        return None
    result = {
        "success": True,
        "file_path": details["image_path"],
        "media_type": "photo",
        "title": details["title"],
        "platform": "Instagram",
        "download_url": url,
        "temp_dir": temp_dir,
    }
    if details.get("audio_path"):
        output = os.path.join(temp_dir, "instagram-photo-video.mp4")
        try:
            await render_photo(
                details["image_path"],
                details["audio_path"],
                output,
                details["start"],
                details["duration"],
            )
            if os.path.getsize(output) > MAX_ASSET_SIZE:
                raise ValueError("Rendered video exceeds upload limit")
            result.update(
                file_path=output,
                media_type="video",
                fallback_image_path=details["image_path"],
            )
        except Exception:
            LOGS.info("Instagram photo rendering failed; using photo", exc_info=True)
    return result
