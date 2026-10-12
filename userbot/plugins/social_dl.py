"""Group and private downloads adapted from the social downloader bot."""

import os
import tempfile

from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message

from userbot import LOGS, SOCKS5_PROXY, UserBot, config
from userbot.helpers.social_access import add_user, is_user_allowed, list_users, remove_user
from userbot.helpers.social_downloader import AUTO_DOWNLOAD_REGEX, detect_platform, download_video
from userbot.plugins.help import add_command_help

MAX_FILE_SIZE = 50 * 1024 * 1024
ENABLED = config.getboolean("social_dl", "enabled", fallback=False)
GROUP_ID = config.getint("social_dl", "allowed_group", fallback=0)
IGNORED_USERS = {
    int(value.strip())
    for value in config.get("social_dl", "ignored_users", fallback="").split(",")
    if value.strip()
}


async def _allowed(bot: UserBot, message: Message) -> bool:
    """Check whether a private sender may use downloads."""
    if not message.from_user:
        return False
    owner = await bot.get_me()
    return await is_user_allowed(bot, message.from_user.id, owner.id, GROUP_ID)


async def _send_photo(bot: UserBot, message: Message, path: str, caption: str) -> None:
    """Send an image or its original document when Telegram rejects the photo."""
    try:
        await bot.send_photo(message.chat.id, path, caption=caption,
                             reply_to_message_id=message.id)
    except BadRequest:
        await bot.send_document(message.chat.id, path, caption=caption,
                                reply_to_message_id=message.id)


async def process_and_upload(bot: UserBot, message: Message, url: str) -> None:
    """Download one link, upload it as a reply, and remove temporary files."""
    platform, _ = detect_platform(url)
    status = await message.reply_text(f"⬇️ Downloading {platform} media...",
                                      disable_notification=True)
    try:
        with tempfile.TemporaryDirectory(prefix="socialdl_") as directory:
            media = await download_video(url, directory, SOCKS5_PROXY)
            path = media["file_path"]
            kind = media.get("media_type", "video")
            if os.path.getsize(path) > MAX_FILE_SIZE and media.get("fallback_image_path"):
                path = media["fallback_image_path"]
                kind = "photo"
            size = os.path.getsize(path)
            if size > MAX_FILE_SIZE:
                raise ValueError(f"Media is too large ({size / 1024 / 1024:.1f}MB; limit 50MB).")
            caption = f"{media['title']}\n{media['download_url']}"[:1024]
            await status.edit_text(f"⬆️ Uploading {kind}...")
            if kind == "photo":
                await _send_photo(bot, message, path, caption)
            else:
                try:
                    await bot.send_video(message.chat.id, path, caption=caption,
                                         reply_to_message_id=message.id,
                                         supports_streaming=True)
                except Exception:
                    if not media.get("fallback_image_path"):
                        raise
                    LOGS.info("Rendered video upload failed; sending photo", exc_info=True)
                    await _send_photo(bot, message, media["fallback_image_path"], caption)
        await status.delete()
    except Exception as error:
        LOGS.exception("Social media download failed")
        await status.edit_text(f"❌ Download failed: {str(error)[:500]}")


@UserBot.on_message(filters.incoming & filters.group & filters.regex(AUTO_DOWNLOAD_REGEX))
async def group_link(bot: UserBot, message: Message) -> None:
    """Auto-download links from others in the configured group."""
    if not ENABLED or message.chat.id != GROUP_ID:
        return
    if message.from_user and message.from_user.id in IGNORED_USERS:
        return
    text = message.text or message.caption or ""
    if text.startswith(("/", ".")):
        return
    _, match = detect_platform(text, auto_only=True)
    if match:
        await process_and_upload(bot, message, match.group(0))


@UserBot.on_message(filters.incoming & filters.private & filters.text, group=1)
async def private_link(bot: UserBot, message: Message) -> None:
    """Handle permitted private links without intercepting commands."""
    if not ENABLED or (message.text or "").startswith(("/", ".")):
        return
    if not await _allowed(bot, message):
        await message.reply_text("You are not authorised to use private downloads.")
        return
    _, match = detect_platform(message.text or "")
    if match:
        await process_and_upload(bot, message, match.group(0))
    else:
        await message.reply_text("Send a TikTok, Instagram, YouTube, or Facebook video link.")


@UserBot.on_message(filters.command("dl", "/"), group=2)
async def slash_download(bot: UserBot, message: Message) -> None:
    """Run a manual download in the configured group or a permitted DM."""
    if not ENABLED or not message.from_user:
        return
    if message.chat.type.name == "PRIVATE" and not await _allowed(bot, message):
        return
    text = " ".join(message.command[1:])
    _, match = detect_platform(text)
    if not match:
        await message.reply_text("Usage: /dl <url>. Supported: TikTok, Instagram, YouTube, Facebook.")
        return
    await process_and_upload(bot, message, match.group(0))


@UserBot.on_message(filters.incoming & filters.command(["start", "help"], "/"))
async def social_help(bot: UserBot, message: Message) -> None:
    """Describe download usage in private chats."""
    if ENABLED:
        await message.reply_text(
            "Send a TikTok, Instagram, YouTube Shorts, YouTube, or Facebook link here. "
            "TikTok, Instagram, and YouTube Shorts download automatically in the configured group. "
            "Use /dl <url> for manual downloads. Private access requires group membership or allowlist access."
        )


@UserBot.on_message(filters.me & filters.command(["allow", "disallow", "allowlist"], [".", "/"]))
async def social_allowlist(bot: UserBot, message: Message) -> None:
    """Manage the private-download allowlist from the owner's account."""
    command = message.command[0].split("@")[0].lstrip("./")
    if command == "allowlist" or (command == "allow" and len(message.command) == 1):
        users = list_users()
        await message.edit_text("Allowed users: " + (", ".join(map(str, users)) or "none"))
        return
    if len(message.command) < 2:
        await message.edit_text(f"Usage: .{command} <user_id>")
        return
    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.edit_text("Invalid user ID.")
        return
    if command == "allow":
        changed = add_user(user_id)
        await message.edit_text("User allowed." if changed else "User already allowed.")
    else:
        changed = remove_user(user_id)
        await message.edit_text("User removed." if changed else "User was not allowed.")


add_command_help(
    "social_dl",
    [
        ["/dl <url>", "Download a supported link in the configured group or permitted private chat."],
        [".allow <user_id>", "Allow private downloads for a user."],
        [".disallow <user_id>", "Remove private download access."],
        [".allowlist", "List permitted private download users."],
    ],
)
