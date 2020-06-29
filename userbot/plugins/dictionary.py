import asyncio

import aiohttp
from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['define', 'dict'], '.') & Filters.me)
async def define(_, message: Message):
    cmd = message.command
    word = ""
    if len(cmd) > 1:
        word = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        word = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`You see I can't just define nothing...`")
        await asyncio.sleep(2)
        await message.delete()
        return

    await message.edit(f"`Defining {word}...`")
    session = aiohttp.ClientSession()
    res = await session.get(f"https://googledictionaryapi.eu-gb.mybluemix.net/?define={word}")
    await session.close()
    if res.status == 200:
        json = await res.json()
        info = json[0].get("meaning")
        if info:
            meaning = ""
            for count, (key, value) in enumerate(info.items(), start=1):
                meaning += f"<b>{count}. {word}</b> <i>({key})</i>\n"
                for i in value:
                    defs = i.get("definition")
                    meaning += f"• <i>{defs}</i>\n"
            await message.edit(meaning, parse_mode='html')
            return
        else:
            await message.edit("`There is no information to display`")
            await asyncio.sleep(3)
            await message.delete()
    else:
        await message.edit("`No results found!`")
        await asyncio.sleep(3)
        await message.delete()


# Command help section
add_command_help(
    'dictionary', [
        ['.define | .dict', 'Define the word you send or reply to.'],
    ]
)
