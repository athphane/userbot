from userbot import BOT
from pyrogram import Filters, Message
from time import sleep


@BOT.on_message(Filters.command(['del', 'delete'], ".") & Filters.me)
def alive(bot: BOT, message: Message):
    reply_message = message.reply_to_message
    try:
        reply_message.delete()
        message.edit("```Message deleted successfully```")
        sleep(2)
        message.delete()
    except:
        message.edit("```Well, I could't delete this message. FFS```")
        sleep(2)
        message.delete()