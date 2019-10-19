from userbot import BOT
from pyrogram import Filters, Message
from userbot.helpers.constants import First


@BOT.on_message(Filters.command("alive", ".") & Filters.me)
def _alive(bot: BOT, message: Message):
    message.edit(First.ALIVE)
