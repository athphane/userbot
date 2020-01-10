from userbot import UserBot
from pyrogram import Filters, Message
import requests
from userbot.plugins.help import add_command_help

DOGBIN = "https://del.dog/"


@UserBot.on_message(Filters.command(['dogbin', 'bin', 'paste'], ".") & Filters.me)
async def dogbin(bot: UserBot, message: Message):
    await message.edit_text("`pasting...`")
    text = message.reply_to_message.text
    try:
        paste = requests.post(f"{DOGBIN}/documents", data=text).json()["key"]
    except requests.exceptions.RequestException as e:
        await message.edit_text("`Pasting failed`")
        print(e)
    else:
        await message.edit_text(f"{DOGBIN}/{paste}", disable_web_page_preview=True)


add_command_help(
    'dogbin', [
        ['.dogbin', 'Create a dogbin paste using replied to message.'],
        ['.bin', 'Alternate command #1'],
        ['.paste', 'Alternate command #2'],
    ]
)
