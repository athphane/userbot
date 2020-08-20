import os

import aiofiles
import aiohttp

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command("qr", prefixes=".") & Filters.me)
async def generate_qr(_, m: Message):
    try:
        if os.path.exists('userbot/downloads/qr.png'):
            os.remove('userbot/downloads/qr.png')
        qr_object = m.text[3:]
        async with aiohttp.ClientSession() as session:
            url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_object}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open('userbot/downloads/qr.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        await m.edit_text("Generating QR...")
        await UserBot.send_photo(m.chat.id, 'userbot/downloads/qr.png')
        await m.delete()
    except exception as e:
        print(e)


add_command_help(
    'qr', [
        ['.qr', 'Generates a qr image of anything you want.\nUsage: `.qr example`'],
    ]
)
