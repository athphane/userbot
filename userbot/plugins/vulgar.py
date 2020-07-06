import asyncio
import re

from pyrogram import Filters, Message
from pyrogram.errors import MessageNotModified

from userbot import UserBot
from userbot.plugins.help import add_command_help

bad_words = ['nigga', 'nigger', 'coon', 'nigg', 'nig']

vulgar_filter = False


def commute():
    global vulgar_filter
    vulgar_filter = not vulgar_filter
    return vulgar_filter


@UserBot.on_message(Filters.command("vulgar", ".") & Filters.me)
async def toggle(_, message: Message):
    c = commute()
    await message.edit("`Vulgar Enabled`" if c else "`Vulgar Disabled`")
    await asyncio.sleep(3)
    await message.delete()


@UserBot.on_message(~Filters.regex(r"^\.\w*") & Filters.me, group=10)
async def i_am_not_allowed_to_say_this(_, message: Message):
    if vulgar_filter:
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

# Command help section
add_command_help(
    'vulgar', [
        ['.vulgar', 'Toggles bad word filtering on and off.'],
    ]
)