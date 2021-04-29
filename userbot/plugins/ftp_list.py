import os
import shutil
from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.helpers.ftp import get_ftp_files
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command("ftp", ".") & filters.me)
async def ftp_list(bot: UserBot, message: Message):
    await message.reply_chat_action('typing')

    await get_ftp_files()

    files = []
    for r, _, f in os.walk("downloads/ftp"):
        for file in f:
            files.append(os.path.join(r, file))

    for f in files:
        await message.reply_chat_action('upload_document')
        await bot.send_document('self', document=f)

    shutil.rmtree('downloads/ftp')

add_command_help(
    "ftp",
    [
        [".ftp", "Crawls your ftp and returns file links"],
    ],
)
