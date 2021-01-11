import os
from random import randint

from pyrogram import filters
from pyrogram.types import Message
from thisapidoesnotexist import get_person, get_cat

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck


@UserBot.on_message((filters.command("person", ".") & filters.me))
async def this_person_does_no_exist(_, message: Message):
    person = get_person()
    file_name = f"{randint(1, 999)}person.jpeg"
    person.save_image(file_name)
    await UserBot.send_photo(
        message.chat.id, file_name, reply_to_message_id=ReplyCheck(message)
    )
    os.remove(file_name)
    await message.delete()


@UserBot.on_message((filters.command("rcat", ".") & filters.me))
async def this_cat_does_no_exist(_, message: Message):
    cat = get_cat()
    file_name = f"{randint(1, 999)}cat.jpeg"
    cat.save_image(file_name)
    await UserBot.send_photo(
        message.chat.id, file_name, reply_to_message_id=ReplyCheck(message)
    )
    os.remove(file_name)
    await message.delete()
