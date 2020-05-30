import re

from pyrogram import Filters, Message

from userbot import UserBot

bad_words = ['nigga', 'nigger', 'coon']


@UserBot.on_message(Filters.me, group=10)
async def i_am_not_allowed_to_say_this(bot: UserBot, message: Message):
    if message.caption:
        txt = message.caption
    elif message.text:
        txt = message.text

    for word in bad_words:
        txt = re.sub(word, 'bruh', txt, flags=re.IGNORECASE)

    if message.caption:
        if txt != message.caption:
            await message.edit_caption(txt)
    elif message.text:
        if txt != message.text:
            await message.edit(txt)
