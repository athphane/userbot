from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters=filters.command("nohello", ".") & filters.me)
async def no_hello(bot: UserBot, message: Message):
    await message.edit('https://nohello.net/en')


# Command help section
add_command_help("nohello", [[".nohello", "Sends the link to the nohello website"]])
