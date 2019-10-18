from userbot import BOT
from pyrogram import Filters, Message
import requests

DOGBIN = "https://del.dog/"


@BOT.on_message(Filters.command(['dogbin', 'bin', 'paste'], ".") & Filters.me)
def dogbin(bot: BOT, message: Message):
    message.edit_text("`pasting...`")
    text = message.reply_to_message.text
    try:
        paste = requests.post(f"{DOGBIN}/documents", data=text).json()["key"]
    except requests.exceptions.RequestException as e:
        message.edit_text("`Pasting failed`")
        print(e)
    else:
        message.edit_text(f"{DOGBIN}/{paste}", disable_web_page_preview=True)
