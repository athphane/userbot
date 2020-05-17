from userbot import UserBot
from pyrogram import Filters, Message
import requests
from userbot.plugins.help import add_command_help


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
        reply_text = f'Nekofied to **Nekobin** : {url}'
        await bot.send_message(
            message.chat.id,
            reply_text,
            disable_web_page_preview=True,
            reply_to_message_id=message.reply_to_message.message_id
        )


add_command_help(
    'paste', [
        ['.paste', 'Create a dogbin paste using replied to message.'],
        ['.bin', 'Alternate command #1'],
    ]
)
