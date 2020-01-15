import re
from time import sleep

from userbot import UserBot
from pyrogram import Filters, Message
import requests

from userbot.helpers.utility import split_list
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


@UserBot.on_message(Filters.command(['getpaste'], ".") & Filters.me)
async def dogbin(bot: UserBot, message: Message):
    link = message.command[1]
    regex = "g\/(\w*)"
    matches = re.search(re.compile(regex), link)
    data = requests.get(f"https://del.dog/raw/{matches.group(1)}").text

    await message.edit("Here are the contents from the paste.")

    if len(data) >= 1024:
        f = open('dogbin.txt', 'w')
        f.write(data)
        f.close()

        await message.reply_document('dogbin.txt', caption=f"```Paste from {link}```")
    else:
        await message.reply(data)

add_command_help(
    'dogbin', [
        ['.dogbin', 'Create a dogbin paste using replied to message.'],
        ['.bin', 'Alternate command #1'],
        ['.paste', 'Alternate command #2'],
    ]
)
