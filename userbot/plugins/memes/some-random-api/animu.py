import asyncio
import re

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.helpers.aiohttp_helper import AioHttp
from userbot.plugins.help import add_command_help

gif_categories = ['wink', 'pat', 'hug', 'face-palm']


@UserBot.on_message(filters.command(["animu-gif", "anime-gif"], ".") & filters.me)
async def animu_gifs(_, message: Message):
    cmd = message.command

    if not (len(cmd) >= 2):
        await message.edit("```Not enough params provided```")
        await asyncio.sleep(3)
        await message.delete()
        return

    if cmd[1].lower() in gif_categories:
        category = cmd[1].lower()

        animu_link = f"https://some-random-api.ml/animu/{category}"

        try:
            data = await AioHttp().get_json(animu_link)
            gif = data["link"]
        except Exception:
            await message.edit(f"```Couldn't get a {category}```")
            await asyncio.sleep(3)
            await message.delete()
        else:
            await message.delete()
            await UserBot.send_animation(
                chat_id=message.chat.id,
                animation=gif,
                reply_to_message_id=ReplyCheck(message)
            )
    else:
        await message.edit("`Unsupported category...`")
        await asyncio.sleep(2)
        await message.delete()


@UserBot.on_message(filters.command(["animu-quote", "anime-quote"], ".") & filters.me)
async def animu_fact(_, message: Message):
    try:
        data = await AioHttp().get_json('https://some-random-api.ml/animu/quote')
    except Exception:
        await message.edit("```Couldn't get an anime quote```")
        await asyncio.sleep(3)
        await message.delete()
    else:
        quote = (
            f"\"{data['sentence'].strip()}\"\n\n"
            f"{data['characther'].strip()} in {data['anime'].strip()}"
        )

        await message.edit(quote)

# Animu gif help
animu_gif_help = []
for x in gif_categories:
    animu_gif_help.append([f".animu-gif {x}", f"Sends a random anime gif of a {x}"])

add_command_help("animu", animu_gif_help)

add_command_help(
    "animu",
    [
        [".animu-quote", f"Send a random anime quote"]
    ],
)
