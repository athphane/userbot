from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

the_regex = r"^r\/([^\s\/])+"

f = filters.chat([])


@UserBot.on_message(f)
async def auto_read(_, message: Message):
    await UserBot.read_history(message.chat.id)
    message.continue_propagation()


@UserBot.on_message(filters.command("autoscroll", ".") & filters.me)
async def add_to_auto_read(_, message: Message):
    if message.chat.id in f:
        f.remove(message.chat.id)
        await message.edit("Autoscroll deactivated")
    else:
        f.add(message.chat.id)
        await message.edit("Autoscroll activated")


# Command help section
add_command_help(
    "autoscroll",
    [
        [
            ".autoscroll",
            "Send .autoscroll in any chat to automatically read all sent messages until you call "
            "autoscroll again. This is useful if you have Telegram open on another screen.",
        ],
    ],
)
