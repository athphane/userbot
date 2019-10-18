from pyrogram import Filters, Message
from userbot import BOT
from userbot.helpers.file_sending_helpers import send_saved_image, send_saved_animation


@BOT.on_message(Filters.command("fast", ".") & Filters.me)
def fast(bot: BOT, message: Message):
    message.edit("Gotta go fast")
    send_saved_image(message, "fast_image", "fast.jpg")


@BOT.on_message(Filters.command(['tfb', 'tbf'], ".") & Filters.me)
def fast(bot: BOT, message: Message):
    send_saved_image(message, "tfb_image", "tfb.jpg")
    message.delete()


@BOT.on_message(Filters.command("kill", ".") & Filters.me)
def kill(bot: BOT, message: Message):
    message.edit("I will kill you")
    send_saved_animation(message, "kill_image", "killua.gif")


@BOT.on_message(Filters.command("dmf", ".") & Filters.me)
def _help(bot: BOT, message: Message):
    send_saved_animation(message, "dmf_image", "dmf.gif")
    message.delete()


@BOT.on_message(Filters.command(['smart', 'intelligence'], ".") & Filters.me)
def _help(bot: BOT, message: Message):
    send_saved_image(message, "intelligence_image", "intelligence.jpg")
    message.delete()
