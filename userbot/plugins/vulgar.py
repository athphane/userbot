import re

from pyrogram import Filters, Message

from userbot import UserBot

bad_words = ['nigga', 'nigger', 'coon']


@UserBot.on_message(Filters.me, group=10)
async def i_am_not_allowed_to_say_this(bot: UserBot, message: Message):
    txt = message.caption if message.caption else message.text

    for word in bad_words:
        txt = re.sub(word, 'bruh', txt, flags=re.IGNORECASE)

    if txt != message.caption if message.caption else message.text:
        try:
            await message.edit(txt)
        except:
            await message.edit_caption(txt)
