from userbot import BOT
from pyrogram import Filters, Message
import os
from time import sleep
from userbot.plugins.help import add_command_help

CARBON_LANG = "py"


@BOT.on_message(Filters.command("carbon", ".") & Filters.me)
def carbon_test(bot: BOT, message: Message):
    """
    Receives text and makes a carbon image using the text
    Eg: .carbon your code here (multi line supported)
    """

    carbon_text = message.text[8:]

    # Write the code to a file cause carbon-now-cli wants a file.
    file = "userbot/downloads/carbon.{}".format(get_carbon_lang())
    f = open(file, "w+")
    f.write(carbon_text)
    f.close()

    message.edit_text("Carbonizing code...")
    # Do the thing
    os.system("carbon-now -h -t userbot/downloads/carbon {}".format(file))
    message.edit_text("Carbonizing completed...")
    # Send the thing
    BOT.send_document(message.chat.id, 'userbot/downloads/carbon.png')
    message.delete()


@BOT.on_message(Filters.command('carbonlang', '.') & Filters.me)
def update_carbon_lang(bot: BOT, message: Message):
    """
    Set language to use Carbon with.
    Eg: .carbonlang js -> will set the file type to js
    """

    global CARBON_LANG
    cmd = message.command

    if len(cmd) > 1:
        type_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        type_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        message.edit("Give me something to carbonize")
        sleep(2)
        message.delete()
        return

    CARBON_LANG = type_text
    message.edit_text("Carbon type set to {}".format(type_text))
    sleep(5)
    message.delete()


@BOT.on_message(Filters.command('carbonlang', '!') & Filters.me)
def send_carbon_lang(bot: BOT, message: Message):
    """
    Edits message to show current set carbon language
    """

    message.edit_text(get_carbon_lang())
    sleep(5)
    message.delete()


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
