from userbot import UserBot
from pyrogram import Filters, Message
from time import sleep

from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['del', 'delete'], ".") & Filters.me)
async def alive(bot: UserBot, message: Message):
    reply_message = message.reply_to_message
    try:
        reply_message.delete()
        await message.edit("```Message deleted successfully```")
        sleep(2)
        await message.delete()
    except:
        await message.edit("```Well, I could't delete this message. FFS```")
        sleep(2)
        await message.delete()


# Command help section
add_command_help(
    'purge', [
        ['.del', 'Deletes the replied to message.'],
    ]
)
