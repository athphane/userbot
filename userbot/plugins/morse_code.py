import asyncio

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

# Dictionary representing the morse code chart
MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-', ' ': '/'}


@UserBot.on_message(filters.command("morse", ".") & filters.me)
async def morse_encrypt(bot: UserBot, message: Message):
    cmd = message.command

    def encrypt(input_string):
        cipher = ''
        for letter in input_string:
            if letter != ' ':
                cipher += MORSE_CODE_DICT[letter] + ' '
            else:
                cipher += ' '

        return cipher

    main_text = ""
    if len(cmd) > 1:
        main_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        main_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("I need something to encrypt")
        await asyncio.sleep(2)
        await message.delete()
        return

    input_str = main_text
    if not input_str:
        await message.edit("`give me something to encrypt`")
        return

    await message.edit(encrypt(input_str.upper()), parse_mode=ParseMode.DISABLED)


@UserBot.on_message(filters.command("morsed", ".") & filters.me)
async def morse_decrypt(bot: UserBot, message: Message):
    cmd = message.command

    def decrypt(input_string):
        input_string += ' '
        decipher = ''
        citext = ''
        for letter in input_string:
            if letter != ' ':
                i = 0
                citext += letter
            else:
                i += 1
                if i == 2:
                    decipher += ' '
                else:
                    decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                    citext = ''

        return decipher

    main_text = ""
    if len(cmd) > 1:
        main_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        main_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("I need something to decrypt")
        await asyncio.sleep(2)
        await message.delete()
        return

    input_str = main_text
    if not input_str:
        await message.edit("`give me something to decrypt`")
        return

    await message.edit(decrypt(input_str).lower(), parse_mode=ParseMode.DISABLED)


# Command help section
add_command_help(
    "morse",
    [
        [".morse", "Encrypt the input text into morse code"],
        [".morsed", "Decrypt morse code to plain text"],
    ],
)
