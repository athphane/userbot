import asyncio
import math
import os

from PIL import Image
from pyrogram import Filters

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(["kang"], '.') & Filters.me)
async def kang_stickers(bot: UserBot, message):
    if not DB_AVAIABLE:
        await message.edit("Your database is not avaiable!")
        return
    sticker_pack = get_sticker_set(message.from_user.id)
    animation_pack = get_stanim_set(message.from_user.id)
    if not sticker_pack:
        await message.edit("You've not set up the sticker pack!\nCheck your assistant for more information!")
        # await setbot.send_message(message.from_user.id,
        #                           "Hello 🙂\nYou're look like want to steal a sticker, but sticker pack was not set. "
        #                           "To set a sticker pack, type /setsticker and follow setup.")
        return
    sticker_pack = sticker_pack.sticker
    if message.reply_to_message and message.reply_to_message.sticker:
        if message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
            if not animation_pack:
                await message.edit(
                    "You're not setup animation sticker pack!\nCheck your assistant for more information!")
                # await setbot.send_message(message.from_user.id,
                #                           "Hello 🙂\nYou're look like want to steal a animation sticker, but sticker "
                #                           "pack was not set. To set a sticker pack, type /setanimation and follow "
                #                           "setup.")
                return
            await bot.download_media(message.reply_to_message.sticker, file_name="nana/cache/sticker.tgs")
        else:
            await bot.download_media(message.reply_to_message.sticker, file_name="nana/cache/sticker.png")
    elif message.reply_to_message and message.reply_to_message.photo:
        await bot.download_media(message.reply_to_message.photo, file_name="nana/cache/sticker.png")
    elif message.reply_to_message and message.reply_to_message.document and message.reply_to_message.document.mime_type == "image/png":
        await bot.download_media(message.reply_to_message.document, file_name="nana/cache/sticker.png")
    else:
        await message.edit(
            "Reply a sticker or photo to kang it!\nCurrent sticker pack is: {}\nCurrent animation pack is: {}".format(
                sticker_pack, animation_pack.sticker))
        return
    if not (
                   message.reply_to_message.sticker and message.reply_to_message.sticker.mime_type) == "application/x-tgsticker":
        im = Image.open("nana/cache/sticker.png")
        maxsize = (512, 512)
        if (im.width and im.height) < 512:
            size1 = im.width
            size2 = im.height
            if im.width > im.height:
                scale = 512 / size1
                size1new = 512
                size2new = size2 * scale
            else:
                scale = 512 / size2
                size1new = size1 * scale
                size2new = 512
            size1new = math.floor(size1new)
            size2new = math.floor(size2new)
            sizenew = (size1new, size2new)
            im = im.resize(sizenew)
        else:
            im.thumbnail(maxsize)
        im.save("nana/cache/sticker.png", 'PNG')

    await bot.send_message("@Stickers", "/addsticker")
    await bot.read_history("@Stickers")
    await asyncio.sleep(0.2)
    if message.reply_to_message.sticker and message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
        await bot.send_message("@Stickers", animation_pack.sticker)
    else:
        await bot.send_message("@Stickers", sticker_pack)
    await bot.read_history("@Stickers")
    await asyncio.sleep(0.2)
    checkfull = await bot.get_history("@Stickers", limit=1)
    if checkfull[
        0].text == 'Whoa! That\'s probably enough stickers for one pack, give it a break. A pack can\'t have more than ' \
                   '120 stickers at the moment.':
        # await message.edit("Your sticker pack was full!\nPlease change one from your Assistant")
        os.remove('nana/cache/sticker.png')
        return
    if message.reply_to_message.sticker and message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
        await bot.send_document("@Stickers", 'nana/cache/sticker.tgs')
        os.remove('nana/cache/sticker.tgs')
    else:
        await bot.send_document("@Stickers", 'nana/cache/sticker.png')
        os.remove('nana/cache/sticker.png')
    try:
        ic = message.text.split(None, 1)[1]
    except:
        try:
            ic = message.reply_to_message.sticker.emoji
        except:
            ic = "🤔"
    if ic is None:
        ic = "🤔"
    await bot.send_message("@Stickers", ic)
    await bot.read_history("@Stickers")
    await asyncio.sleep(1)
    await bot.send_message("@Stickers", "/done")
    if message.reply_to_message.sticker and message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
        await message.edit(
            "**Animation Sticker added!**\nYour animated sticker has been saved on [This sticker animated pack]("
            f"https://t.me/addstickers/{animation_pack.sticker})")
    else:
        await message.edit(
            f"**Sticker added!**\nYour sticker has been saved on [This sticker pack](https://t.me/addstickers/{sticker_pack})")
    await bot.read_history("@Stickers")


add_command_help(
    'restart', [
        ['.restart', 'You are retarded if you do not know what this does.'],
        ['.restart g', 'Pull latest changes from git repo and restarts.'],
        ['.restart p', 'Installs pip requirements restarts.'],
        ['.restart gp', 'Pull latest changes from git repo, install pip requirements and restarts.'],
    ]
)
