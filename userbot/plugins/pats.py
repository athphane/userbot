import asyncio

import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck, GetChatID
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command(["pat", "pats"], ".") & filters.me)
async def give_pats(_, message: Message):
    URL = "https://some-random-api.ml/animu/pat"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.edit("`no Pats for you :c")
            result = await request.json()
            url = result.get("link", None)
            await asyncio.gather(
                message.delete(),
                UserBot.send_video(
                    GetChatID(message), url, reply_to_message_id=ReplyCheck(message)
                ),
            )


# Command help section
add_command_help(
    "pats",
    [
        [".pat | .pats", "Give pats."],
    ],
)
