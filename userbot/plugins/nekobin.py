import asyncio

import requests
from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['bin', 'paste'], ".") & Filters.me)
async def paste(bot: UserBot, message: Message):
    await message.edit_text("`Pasting...`")
    text = message.reply_to_message.text
    try:
        key = requests.post('https://nekobin.com/api/documents', json={"content": text}).json().get('result').get('key')
    except requests.exceptions.RequestException as e:
        await message.edit_text("`Pasting failed`")
        await asyncio.sleep(2)
        await message.delete()
    else:
        url = f'https://nekobin.com/{key}'
        reply_text = f'Nekofied to **Nekobin** : {url}'
        await message.edit_text(
            reply_text,
            disable_web_page_preview=True,
        )


add_command_help(
    'paste', [
        ['.paste `or` .bin', 'Create a Nekobin paste using replied to message.'],
    ]
)
