import asyncio

import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from userbot import UserBot
from userbot import YANDEX_API_KEY
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command(['tr', 'trans'], '.') & filters.me)
async def translate(_, message: Message):
    if not YANDEX_API_KEY:
        await message.edit("NO API KEY found in configuration. Get one from https://tech.yandex.com/translate/",
                           disable_web_page_preview=True)
        return

    if message.reply_to_message:
        txt = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        txt = " ".join(message.command[1:])
    else:
        await message.edit("Nothing to translate")
        await asyncio.sleep(3)
        await message.delete()
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://translate.yandex.net/api/v1.5/tr.json/translate?key={YANDEX_API_KEY}&text={txt}&lang=en") as resp:
            result = await resp.json()

            if "message" in result:
                await message.edit(result["message"])
                await asyncio.sleep(3)
                await message.delete()
            else:
                translated = "<b>Original Text:</b>\n" \
                             f"{txt}\n\n" \
                             "<b>Translated Text:</b>\n" \
                             f"{result['text'].pop()}"
                await message.edit(translated)


@UserBot.on_message(filters.command("yoda", ".") & filters.me)
async def yoda(_, message: Message):
    if message.reply_to_message:
        txt = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        txt = " ".join(message.command[1:])
    else:
        await message.edit("Nothing to translate")
        await asyncio.sleep(3)
        await message.delete()
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.funtranslations.com/translate/yoda.json?text={txt}") as resp:
            result = await resp.json()

            if "error" in result:
                await message.edit(result['error']['message'])
                await asyncio.sleep(5)
                await message.delete()
            else:
                translated = result['contents']['translated']
                await message.edit(translated)


add_command_help(
    'translate', [
        ['.tr `or` .trans', 'Translate text to English.'],
        ['.yoda', 'Like Yoda, speak.']
    ]
)
