import os
import cv2
from pyzbar import pyzbar

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

@UserBot.on_message(Filters.command("decode", prefixes=".") & Filters.me)
async def qr_decode(_, m:Message):
    try:
        if os.path.exists('userbot/downloads/qr_decode.png'):
            os.remove('userbot/downloads/qr_decode.png')
        image = await m.reply_to_message.download("userbot/downloads/qr_decode.png")
        await m.edit_text("Decoding QR...")
        output = await read_qr(image)
        await m.edit_text(output)
    except exception as e:
        await UserBot.send_message(m.chat.id, f"Oopsie I encountered an error: {e}.")
        print(e)


async def read_qr(image):
    im_gray = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    im_bw = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_bw = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY)[1]
    barcodes = pyzbar.decode(im_bw)
    return barcodes[0].data.decode('utf-8')


add_command_help(
    'qr', [
        ['.qr', 'Generates a qr image of anything you want.\nUsage: `.qr example`'],
        ['.decode', 'Reply to a qr image to decode it.'],
    ]
)
