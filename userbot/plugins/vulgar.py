import asyncio
import re

from pyrogram import filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import Message

from userbot import LOGS, UserBot
from userbot.plugins.help import add_command_help

bad_words = ["nigga", "nigger", "coon", "cock", "kiss"]
good_words = ["black person", "black person", "bruh", "coke", "keys"]
vulgar_filter = True


def switch():
    global vulgar_filter
    vulgar_filter = not vulgar_filter
    return vulgar_filter


@UserBot.on_message(filters.command("vulgar", ".") & filters.me)
async def toggle(bot: UserBot, message: Message):
    c = switch()
    await message.edit("`Vulgar Enabled`" if c else "`Vulgar Disabled`")
    await asyncio.sleep(3)
    await message.delete()


@UserBot.on_message(~filters.regex(r"^\.\w*") & filters.me & ~filters.media, group=10)
async def i_am_not_allowed_to_say_this(bot: UserBot, message: Message):
    if vulgar_filter:
        try:
            txt = None
            if message.caption:
                txt = message.caption
            elif message.text:
                txt = message.text

            for word in bad_words:
                try:
                    txt = re.sub(word, good_words[bad_words.index(word)], txt, flags=re.IGNORECASE)
                except Exception as e:
                    LOGS.warn(e)

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
    "vulgar",
    [
        [".vulgar", "Toggles bad word filtering on and off."],
    ],
)
