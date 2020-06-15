from random import randint

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help

@UserBot.on_message(Filters.command('person', '.') & Filters.me)
async def send_person(bot: BOT, message: Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://thispersondoesnotexist.com/image?randomtag=" + str(randint(0,9999)),
        caption="persono",
        reply_to_message_id=ReplyCheck(message)
    )
    await message.delete()
