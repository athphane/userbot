import asyncio

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

QUOTLY_BOT = "@QuotLyBot"
POLL_INTERVAL = 2
MAX_POLLS = 15


@UserBot.on_message(filters.me & filters.command(["q", "quote"], "."))
async def quotly(bot: UserBot, message: Message):
    if not message.reply_to_message:
        await message.edit("Reply to any user's text message")
        return

    # Single-line ``` blocks parse as an empty message in Kurigram, so use inline code.
    await message.edit("`Making a quote...`")

    forwarded = await message.reply_to_message.forward(QUOTLY_BOT)

    for attempt in range(1, MAX_POLLS + 1):
        await asyncio.sleep(POLL_INTERVAL)
        latest = [item async for item in bot.get_chat_history(QUOTLY_BOT, limit=1)]
        # Only accept a sticker that arrived after our forward, not an old quote.
        if latest and latest[0].sticker and latest[0].id > forwarded.id:
            await asyncio.gather(
                message.delete(),
                bot.forward_messages(message.chat.id, QUOTLY_BOT, latest[0].id),
            )
            return
        await message.edit(f"`Making a quote... {attempt * 100 // MAX_POLLS}%`")

    await message.edit("`QuotLyBot did not respond in time`")


# Command help section
add_command_help(
    "quotly",
    [
        [".q | .quote", "Make a quote with reply to message."],
    ],
)
