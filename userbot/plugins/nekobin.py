import asyncio
import aiohttp
import requests
from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['neko', 'nekobin', 'bin', 'paste'], ".") & Filters.me)
async def paste(bot: UserBot, message: Message):
    await message.edit_text("`Pasting...`")
    text = message.reply_to_message.text
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://nekobin.com/api/documents',
                json={"content": text},
                timeout=3
            ) as response:
                key = (await response.json())["result"]["key"]
    except Exception:
        await message.edit_text("`Pasting failed`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        url = f'https://nekobin.com/{key}'
        reply_text = f'Nekofied to **Nekobin** : {url}'
        await message.edit_text(
            reply_text,
            disable_web_page_preview=True,
        )

        if len(message.command) > 1 and message.command[1] in ['d', 'del']:
            if message.reply_to_message.from_user.is_self:
                await message.reply_to_message.delete()


add_command_help(
    'paste', [
        ['.paste `or` .bin `or` .neko `or` .nekobin', 'Create a Nekobin paste using replied to message.'],
    ]
)
