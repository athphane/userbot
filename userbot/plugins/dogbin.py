from userbot import BOT
from pyrogram import Filters, Message
import requests
from userbot.plugins.help import add_command_help

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


add_command_help(
    'dogbin', [
        ['.dogbin', 'Show the creator of this userbot.'],
        ['.bin', 'Show the creator of this userbot.'],
        ['.paste', 'Show the creator of this userbot.'],
    ]
)
