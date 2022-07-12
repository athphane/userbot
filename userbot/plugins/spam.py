import asyncio

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command("spam", ".") & filters.me)
async def spam(bot: UserBot, message: Message):
    # Get current chat and spam to there.
    # if in group and replied to user, then spam replying to user.
    await message.delete()

    times = message.command[1]
    to_spam = " ".join(message.command[2:])

    for _ in range(int(times)):
        await bot.send_message(message.chat.id, to_spam, reply_to_message_id=ReplyCheck(message))
        await asyncio.sleep(0.20)


# Command help section
add_command_help("spam", [[".spam", "<spam_amount> <spam_text>"]])
