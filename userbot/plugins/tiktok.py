import asyncio
import os

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.helpers.tiktokHelper import TikTok
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command(['t', 'tiktok'], '.') & filters.me)
async def download_tiktok(bot: UserBot, message: Message):
    if message.reply_to_message:
        txt = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        txt = " ".join(message.command[1:])
    else:
        await message.edit("TikTok link not found")
        await asyncio.sleep(3)
        await message.delete()
        return

    try:
        await message.edit("Processing link...")
        tiktok_video = await TikTok.download_tiktok(txt)
        await bot.send_video(message.chat.id, tiktok_video, supports_streaming=True)
        await message.delete()
        os.remove(tiktok_video)
        return

    except Exception as e:
        print(e)
        await message.edit("Error while processing tiktok link")
        await asyncio.sleep(3)
        await message.delete()
        return


add_command_help(
    "tiktok",
    [[".t or .tiktok", "given a link to a tiktok video download and send it"]],
)
