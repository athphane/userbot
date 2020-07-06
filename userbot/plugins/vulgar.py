import re

from pyrogram import Filters, Message
from pyrogram.errors import MessageNotModified

from userbot import UserBot

bad_words = ['nigga', 'nigger', 'coon', 'nigg', 'nig']


def vulgar_switch(self):
    """Switch states between `True` and `False`"""
    self.flag = not self.flag
    return self.flag


f = Filters.create(lambda self, _: self.flag, flag=True, commute=vulgar_switch)


@UserBot.on_message(Filters.command("vulgar", ".") & Filters.me)
async def toggle(_, message: Message):
    c = f.commute()
    await message.reply_text("`Vulgar Enabled`" if c else "`Vulgar Disabled`")


@UserBot.on_message(f & ~Filters.regex(r"^\.\w*") & Filters.me, group=10)
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
