from userbot import BOT
from pyrogram import Filters, Message


# @BOT.on_message(Filters.command('fry', ".") & Filters.me)
# def fry(bot: BOT, message: Message):
#     reply_mesage = message.reply_to_message
#     print(reply_mesage.photo.file_ref)
#
#     if reply_mesage.photo is None:
#         message.edit("Reply to a picture to fry it")
#         return
#
#     photo_path = BOT.download_media(reply_mesage, file_ref=reply_mesage.photo.file_ref)


