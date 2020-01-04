from userbot import UserBot
from pyrogram import Filters, Message
from userbot.helpers.constants import First
from userbot.plugins.help import add_command_help
import time


@UserBot.on_message(Filters.command("spam", ".") & Filters.me)
async def alive(bot: UserBot, message: Message):
    # Get current chat and spam to there.
    # if in group and replied to user, then spam replying to user.
    times = message.command[1]
    to_spam = message.command[2]

    if message.chat.type in ['supergroup', 'group'] and message.reply_to_message:
        for x in range(int(times)):
            await bot.send_message(message.chat.id, to_spam, reply_to_message_id=message.reply_to_message.message_id)
            time.sleep(0.15)

    if message.chat.type is "private":
        for x in range(int(times)):
            await bot.send_message(message.chat.id, to_spam)
            time.sleep(0.15)


# Command help section
add_command_help(
    'spam', [['.spam', 'Spam something.']]
)
