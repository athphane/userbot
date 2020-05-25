import aiohttp
import asyncio
from userbot import UserBot
from userbot import YANDEX_API_KEY
from pyrogram import Filters, Message
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command("tr", ".") & Filters.me)
async def translate(bot: UserBot, message: Message):
    if not YANDEX_API_KEY:
        await message.edit("NO API KEY found in configuration. Get one from https://tech.yandex.com/translate/", disable_web_page_preview=True)
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
        async with session.get(f"https://translate.yandex.net/api/v1.5/tr.json/translate?key={YANDEX_API_KEY}&text={txt}&lang=en") as resp:
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

@UserBot.on_message(Filters.command("yoda", ".") & Filters.me)
async def yoda(bot: UserBot, message: Message):
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
        ['.tr', 'Translate text to English'],
        ['.yoda', 'Translate text to Yoda']
    ]
)
