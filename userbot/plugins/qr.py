import cv2
import qrcode
from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command('qr', '.') & filters.me)
async def generate_qr(_, message: Message):
    if qr_text := await UserBot.extract_command_text(message):
        img = qrcode.make(qr_text)

        with open('downloads/qr.png', 'wb') as f:
            img.save(f)

        await message.reply_photo('downloads/qr.png')


@UserBot.on_message(filters.command('qrscan', '.') & filters.reply & filters.me)
async def scan_qr(_, message: Message):
    await message.reply_to_message.download('downloads/qr.png')
    img = cv2.imread('downloads/qr.png')
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    await message.edit_text(data)


# Command help section
add_command_help(
    "qr",
    [
        [".qr", "Generate QR codes for given input."],
        [".qrscan", "Scan a QR code and send it's contents."],
    ],
)
