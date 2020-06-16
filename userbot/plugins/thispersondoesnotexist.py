import os
from random import randint

from pyrogram import Filters, Message
from thisapidoesnotexist import get_person

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck


@UserBot.on_message((Filters.command('person', '.') & Filters.me))
async def this_person_does_no_exist(bot: UserBot, message: Message):
    person = get_person()
    file_name = f"{randint(1, 999)}person.jpeg"
    person.save_image(file_name)
    await bot.send_photo(message.chat.id, file_name, reply_to_message_id=ReplyCheck(message))
    os.remove(file_name)
    await message.delete()
