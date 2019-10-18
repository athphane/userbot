from userbot import BOT
from pyrogram import Filters, Message
from userbot.helpers.constants import First


@BOT.on_message(Filters.command("alive", ".") & Filters.me)
def _alive(bot: BOT, message: Message):
    message.edit(First.ALIVE)


# @BOT.on_message(Filters.command("slap", ".") & Filters.me)
# def slap(bot: BOT, message: Message):
#     victim = message.reply_to_message.from_user
#     victim = get_user_mentionable(victim)
#     message.delete()
#     BOT.send_message(message.chat.id, f'Slaps {victim} with a smelly trout.')


