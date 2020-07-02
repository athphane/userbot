import os
from userbot import UserBot
from pyrogram import Client, Filters, Message

import PIL.Image as Image
from nsfw import classify


@UserBot.on_message(Filters.command("nude", prefixes='.') & Filters.me)
def check_nudity(bot: UserBot, message: Message):
    if os.path.exists("downloads/image_ml.jpg"):
        os.remove("downloads/image_ml.jpg")

    bot.download_media(
        message=message.reply_to_message.photo.file_id,
        file_name="image_ml.jpg"
    )

    image = Image.open("downloads/image_ml.jpg")
    sfw, nsfw = classify(image)

    if nsfw > sfw:
        stat = True
    else:
        stat = False

    bot.edit_message_text(
        message.chat.id,
        message.message_id,
        "<b>Image Stats: </b>\n<b>sfw score:</b> <i>{0}</i>"
        "<b>nsfw score:</b> <i>{1}</i>\n<b>Is Nude:</b> <i>{2}</i>".format(
            sfw, nsfw, stat),
        "html"
    )
