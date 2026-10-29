"""Shared Instagram album uploads."""

from pyrogram.enums import ParseMode
from pyrogram.errors import BadRequest
from pyrogram.types import InputMediaPhoto, ReplyParameters


async def send_photos(bot, chat_id, reply_id, file_paths, caption):
    """Send ordered albums of up to ten photos, with one caption per post."""
    for start in range(0, len(file_paths), 10):
        batch = file_paths[start:start + 10]
        batch_caption = caption if start == 0 else ""
        if len(batch) == 1:
            await send_photo(bot, chat_id, reply_id, batch[0], batch_caption)
            continue
        try:
            await bot.send_media_group(chat_id, [
                InputMediaPhoto(path, caption=batch_caption if index == 0 else "",
                                parse_mode=ParseMode.DISABLED)
                for index, path in enumerate(batch)
            ], reply_parameters=ReplyParameters(message_id=reply_id) if reply_id else None)
        except BadRequest:
            # Preserve the existing document fallback for rejected images.
            for index, path in enumerate(batch):
                await send_photo(bot, chat_id, reply_id, path, batch_caption if index == 0 else "")


async def send_photo(bot, chat_id, reply_id, path, caption):
    """Fall back to the original document for rejected photos."""
    options = dict(caption=caption, parse_mode=ParseMode.DISABLED,
                   reply_parameters=ReplyParameters(message_id=reply_id) if reply_id else None)
    try:
        await bot.send_photo(chat_id, path, **options)
    except BadRequest:
        await bot.send_document(chat_id, path, **options)
