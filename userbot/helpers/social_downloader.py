"""Download and prepare social media for Telegram uploads."""

import asyncio
import json
import logging
import os
import re

import aiohttp

from userbot.helpers.instagram import download_instagram_photo, run_process

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
YOUTUBE_SHORTS_REGEX = r"https?://(?:www\.)?youtube\.com/shorts/[\w-]+/?(?:\?[^\s]*)?"
YOUTUBE_REGEX = (
    r"https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/|embed/|v/)|"
    r"youtu\.be/)[\w-]+/?(?:\?[^\s]*)?"
)
INSTAGRAM_REGEX = (
    r"https?://(?:www\.)?(?:instagram\.com|ddinstagram\.com|"
    r"kkinstagram\.com)/(?:p|reels|reel|tv|stories|share/reel|share/p)/[\w-]+/?"
)
TIKTOK_REGEX = (
    r"https?://(?:www\.|vm\.|vt\.|t\.)?tiktok\.com/"
    r"(?:@[\w.-]*/video/\d+|@/video/\d+|[\w]+/?)[^\s]*"
)
FACEBOOK_REGEX = (
    r"https?://(?:www\.|m\.|web\.)?facebook\.com/"
    r"(?:watch/?\?v=\d+|[\w.-]+/videos/\d+|reel/\d+|"
    r"share/(?:v|r)/\d+|[\w.-]+/posts/\d+)/?[^\s]*"
)
AUTO_DOWNLOAD_REGEX = f"(?:{INSTAGRAM_REGEX}|{TIKTOK_REGEX}|{YOUTUBE_SHORTS_REGEX})"
ALL_PLATFORMS_REGEX = f"(?:{AUTO_DOWNLOAD_REGEX}|{YOUTUBE_REGEX}|{FACEBOOK_REGEX})"
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".webm", ".mov", ".m4v", ".avi"}
LOGGER = logging.getLogger(__name__)


def detect_platform(text: str, auto_only: bool = False):
    """Find the first supported URL and return its platform and match."""
    patterns = [
        ("Instagram", INSTAGRAM_REGEX),
        ("TikTok", TIKTOK_REGEX),
        ("YouTube Shorts", YOUTUBE_SHORTS_REGEX),
    ]
    if not auto_only:
        patterns += [("YouTube", YOUTUBE_REGEX), ("Facebook", FACEBOOK_REGEX)]
    matches = [(match.start(), name, match) for name, pattern in patterns
               if (match := re.search(pattern, text, re.IGNORECASE))]
    if not matches:
        return None, None
    _, name, match = min(matches, key=lambda item: item[0])
    return name, match


async def normalise_url(url: str) -> str:
    """Resolve short links and replace Instagram front-end domains."""
    if "youtube.com" not in url and "youtu.be" not in url:
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout, headers={"User-Agent": USER_AGENT}) as session:
                async with session.head(url, allow_redirects=True) as response:
                    if response.status == 200:
                        url = str(response.url)
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass
    return url.replace("ddinstagram.com", "instagram.com").replace(
        "kkinstagram.com", "instagram.com"
    )


def download_error(stderr: bytes, platform: str) -> str:
    """Return the useful final error from yt-dlp output."""
    output = stderr.decode("utf-8", errors="replace")
    if "HTTP Error 429" in output or "Too Many Requests" in output:
        return f"{platform} is rate-limiting this server (HTTP 429). Please try again later."
    errors = [line.removeprefix("ERROR: ") for line in output.splitlines()
              if line.startswith("ERROR:")]
    return (errors[-1] if errors else output.strip())[-500:] or "yt-dlp failed."


async def prepare_telegram_video(video_path: str) -> str:
    """Convert YouTube media to a streamable H.264/AAC MP4."""
    code, stdout, stderr = await run_process(
        "ffprobe", "-v", "error", "-show_streams", "-of", "json", video_path
    )
    if code:
        raise RuntimeError(f"Video inspection failed: {stderr.decode(errors='replace')[:400]}")
    streams = json.loads(stdout)["streams"]
    video = next((stream for stream in streams if stream["codec_type"] == "video"), None)
    audio = next((stream for stream in streams if stream["codec_type"] == "audio"), None)
    if video is None:
        raise RuntimeError("Downloaded file contains no video stream.")
    output = os.path.join(os.path.dirname(video_path), "telegram.mp4")
    args = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", video_path,
            "-map", "0:v:0", "-map", "0:a:0?"]
    if video.get("codec_name") == "h264" and video.get("pix_fmt") == "yuv420p":
        args.extend(["-c:v", "copy"])
    else:
        args.extend(["-c:v", "libx264", "-preset", "fast", "-crf", "23",
                     "-pix_fmt", "yuv420p", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2"])
    args.extend(["-c:a", "copy" if audio and audio.get("codec_name") == "aac" else "aac",
                 "-movflags", "+faststart", output])
    code, _, stderr = await run_process(*args)
    if code or not os.path.isfile(output) or not os.path.getsize(output):
        raise RuntimeError(f"MP4 conversion failed: {stderr.decode(errors='replace')[:400]}")
    return output


async def download_video(url: str, directory: str, proxy: str | None = None) -> dict:
    """Download a supported URL into directory and return upload metadata."""
    download_url = await normalise_url(url)
    platform, _ = detect_platform(download_url)
    if platform is None:
        raise ValueError("Unsupported URL or platform.")
    args = ["yt-dlp", "--user-agent", USER_AGENT, download_url, "-o",
            os.path.join(directory, "%(title)s [%(id)s].%(ext)s")]
    if platform in {"YouTube", "YouTube Shorts"}:
        args.extend(["--no-playlist", "-S", "vcodec:h264,acodec:aac"])
    if proxy:
        args.extend(["--proxy", proxy])
    try:
        code, _, stderr = await run_process(*args)
        if code and b"CERTIFICATE_VERIFY_FAILED" in stderr:
            code, _, stderr = await run_process(*(args + ["--no-check-certificate"]))
        if code:
            raise RuntimeError(download_error(stderr, platform))
        files = [name for name in os.listdir(directory)
                 if os.path.splitext(name)[1].lower() in VIDEO_EXTENSIONS]
        if not files:
            raise RuntimeError("No video files were downloaded.")
        file_path = os.path.join(directory, files[0])
        title = os.path.splitext(files[0])[0].split(" [")[0]
        if platform in {"YouTube", "YouTube Shorts"}:
            file_path = await prepare_telegram_video(file_path)
        return {"file_path": file_path, "media_type": "video", "title": title,
                "download_url": download_url}
    except Exception:
        if platform == "Instagram":
            try:
                photo = await download_instagram_photo(download_url, directory, proxy, USER_AGENT)
                if photo:
                    return photo
            except Exception:
                LOGGER.info("Instagram photo fallback failed", exc_info=True)
        raise
