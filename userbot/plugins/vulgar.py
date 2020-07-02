import re

from pyrogram import Filters, Message
from pyrogram.errors import MessageNotModified

from userbot import UserBot

bad_words = ['nigga', 'nigger', 'coon']


@UserBot.on_message(~Filters.regex(r"^\.\w*") & Filters.me, group=10)
async def i_am_not_allowed_to_say_this(_, message: Message):
    try:
        txt = None
        if message.caption:
            txt = message.caption
        elif message.text:
            txt = message.text

        for word in bad_words:
            try:
                txt = re.sub(word, 'bruh', txt, flags=re.IGNORECASE)
            except Exception:
                pass

        if message.caption:
            if txt != message.caption:
                await message.edit_caption(txt)

        elif message.text:
            if txt != message.text:
                await message.edit(txt)
    except MessageNotModified:
        return
