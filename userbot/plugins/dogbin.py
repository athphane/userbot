import re
from userbot import UserBot
from pyrogram import Filters, Message
import requests
from userbot.plugins.help import add_command_help

DOGBIN = "https://del.dog/"


@UserBot.on_message(Filters.command(['bin', 'paste'], ".") & Filters.me)
async def paste(bot: UserBot, message: Message):
    await message.edit_text("`Pasting...`")
    text = message.reply_to_message.text
    try:
        key = requests.post('https://nekobin.com/api/documents', json={"content": text}).json().get('result').get('key')
    except requests.exceptions.RequestException as e:
        await message.edit_text("`Pasting failed`")
    else:
        url = f'https://nekobin.com/{key}'
        reply_text = f'Nekofied to *Nekobin* : {url}'
        await message.edit_text(reply_text, disable_web_page_preview=True)


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
