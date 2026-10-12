"""Opt-in downloads for links sent by other people."""

import os
import tempfile

from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message

from userbot import LOGS, SOCKS5_PROXY, UserBot
from userbot.helpers.social_chats import is_chat_enabled, list_chats, set_chat_enabled
from userbot.helpers.social_downloader import AUTO_DOWNLOAD_REGEX, detect_platform, download_video
from userbot.plugins.help import add_command_help

MAX_FILE_SIZE = 50 * 1024 * 1024


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
    """Auto-download links from others in enabled groups."""
    if not is_chat_enabled(message.chat.id):
        return
    text = message.text or message.caption or ""
    if text.startswith(("/", ".")):
        return
    _, match = detect_platform(text, auto_only=True)
    if match:
        await process_and_upload(bot, message, match.group(0))


@UserBot.on_message(filters.incoming & filters.private, group=1)
async def private_link(bot: UserBot, message: Message) -> None:
    """Handle links sent by others in enabled private chats."""
    if not is_chat_enabled(message.chat.id):
        return
    text = message.text or message.caption or ""
    if text.startswith(("/", ".")):
        return
    _, match = detect_platform(text)
    if match:
        await process_and_upload(bot, message, match.group(0))


@UserBot.on_message(filters.me & filters.command("socialdl", "."))
async def social_chat_settings(bot: UserBot, message: Message) -> None:
    """Let the owner enable or disable downloads in the current chat."""
    action = message.command[1].lower() if len(message.command) > 1 else "status"
    chat_id = message.chat.id
    if action == "list":
        chats = list_chats()
        await message.edit_text(
            "Enabled chats: " + (", ".join(map(str, chats)) or "none")
        )
    elif action in {"on", "off"}:
        set_chat_enabled(chat_id, action == "on")
        state = "enabled" if action == "on" else "disabled"
        await message.edit_text(f"Social downloads {state} here.")
    elif action == "status":
        state = "enabled" if is_chat_enabled(chat_id) else "disabled"
        await message.edit_text(f"Social downloads are {state} here.")
    else:
        await message.edit_text("Usage: .socialdl on|off|status|list")


add_command_help(
    "social_dl",
    [
        [".socialdl on|off", "Enable or disable downloads for other senders in this chat."],
        [".socialdl status|list", "Show this chat's setting or all enabled chat IDs."],
    ],
)
