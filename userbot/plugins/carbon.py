"""
Receives text or code and makes a carbon image using it
"""

import os

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.helpers.carbon_client import carbon_client
from userbot.plugins.help import add_command_help

CARBON_LANG = "py"


@UserBot.on_message(filters.command("carbon", ".") & filters.me)
async def carbon_test(bot: UserBot, message: Message):
    """
    Receives text and makes a carbon image using the text
    Eg: .carbon your code here (multi line supported)
    """
    code_to_carbonize = ""

    carbon_text = message.text[8:]
    if message.reply_to_message and message.reply_to_message.text:
        code_to_carbonize = message.reply_to_message.text
    elif len(carbon_text) > 0:
        code_to_carbonize = message.command[1]
    else:
        # top secret https://tinyurl.com/Donbestupid
        await message.edit_text(
            "Where's the code bruh? Reply to a code or provide it after `.carbon`"
        )
        return

    await message.edit_text("Carbonizing code...")

    # Do the thing boom
    client = carbon_client()
    img = await client.create(code_to_carbonize)
    await message.edit_text("Carbonizing completed...")
    # Send the thing
    await bot.send_photo(message.chat.id, img)
    await message.delete()
    # Remove the generated image after sending it
    os.remove(img)


# since the carbon api has auto language detection i thought this is not necessary anymore
# @UserBot.on_message(filters.command("carbonlang", ".") & filters.me)
# async def update_carbon_lang(bot: UserBot, message: Message):
#     """
#     Set language to use Carbon with.
#     Eg: .carbonlang js -> will set the file type to js
#     """
#     global CARBON_LANG
#     cmd = message.command

#     type_text = ""
#     if len(cmd) > 1:
#         type_text = " ".join(cmd[1:])
#     elif message.reply_to_message and len(cmd) == 1:
#         type_text = message.reply_to_message.text
#     elif not message.reply_to_message and len(cmd) == 1:
#         await message.edit("Give me something to carbonize")
#         await sleep(2)
#         await message.delete()
#         return

#     CARBON_LANG = type_text
#     await message.edit_text("Carbon type set to {}".format(type_text))
#     await sleep(2)
#     await message.delete()


# @UserBot.on_message(filters.command("carbonlang", "!") & filters.me)
# async def send_carbon_lang(bot: UserBot, message: Message):
#     """
#     Edits message to show current set carbon language
#     """
#     await message.edit_text(get_carbon_lang())
#     await sleep(5)
#     await message.delete()


# def get_carbon_lang():
#     """
#     Gets carbon language. Default py
#     """
#     return CARBON_LANG


add_command_help(
    "carbon",
    [
        [
            ".carbon",
            "Generates a carbon image of your code.\nUsage: `.carbon` reply to message or command args",
        ],
        # [
        #     ".carbonlang",
        #     "Change carbon language for syntax highlighting.\nUsage: `.carbonlang` reply to message or "
        #     "command args\n"
        #     "Please use file extensions for best results.",
        # ],
        # [
        #     "!carbonlang",
        #     "Show current carbon language. Default is python.\nUsage: `!carbonlang`",
        # ],
    ],
)
