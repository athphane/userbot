import os
from asyncio import sleep

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

CARBON_LANG = "py"


@UserBot.on_message(filters.command("carbon", ".") & filters.me)
async def carbon_test(_, message: Message):
    """
    Receives text and makes a carbon image using the text
    Eg: .carbon your code here (multi line supported)
    """
    carbon_text = message.text[8:]

    # Write the code to a file cause carbon-now-cli wants a file.
    file = "userbot/downloads/carbon.{}".format(get_carbon_lang())
    with open(file, "w+") as f:
        f.write(carbon_text)

    await message.edit_text("Carbonizing code...")
    # Do the thing
    os.system("carbon-now -h -t userbot/downloads/carbon {}".format(file))
    # await message.edit_text("Carbonizing completed...")
    # Send the thing
    await UserBot.send_photo(message.chat.id, 'userbot/downloads/carbon.png')
    await message.delete()


@UserBot.on_message(filters.command('carbonlang', '.') & filters.me)
async def update_carbon_lang(_, message: Message):
    """
    Set language to use Carbon with.
    Eg: .carbonlang js -> will set the file type to js
    """
    global CARBON_LANG
    cmd = message.command

    type_text = ""
    if len(cmd) > 1:
        type_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        type_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("Give me something to carbonize")
        await sleep(2)
        await message.delete()
        return

    CARBON_LANG = type_text
    await message.edit_text("Carbon type set to {}".format(type_text))
    await sleep(2)
    await message.delete()


@UserBot.on_message(filters.command('carbonlang', '!') & filters.me)
async def send_carbon_lang(_, message: Message):
    """
    Edits message to show current set carbon language
    """
    await message.edit_text(get_carbon_lang())
    await sleep(5)
    await message.delete()


def get_carbon_lang():
    """
    Gets carbon language. Default py
    """
    return CARBON_LANG


add_command_help(
    'carbon', [
        ['.carbon', 'Generates a carbon image of your code.\nUsage: `.carbon` reply to message or command args'],
        ['.carbonlang', 'Change carbon language for syntax highlighting.\nUsage: `.carbonlang` reply to message or '
                        'command args\n'
                        'Please use file extensions for best results.'],
        ['!carbonlang', 'Show current carbon language. Default is python.\nUsage: `!carbonlang`'],
    ]
)
