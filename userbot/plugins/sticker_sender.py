from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot

SETS = {
    1: [
        'CAACAgUAAxkDAAI4IGEOvOVBnkzKf6MQCgvsJuGk5PRbAAKYAgACf1BBV4xU-M-oahBJHgQ',
        'CAACAgUAAxkDAAI4IWEOvOZKgAYskiJ3gcu6InBogwnkAAJKAwACmd1BV4c0knnsItszHgQ',
        'CAACAgUAAxkDAAI4ImEOvOmcilCfnLmTxOGZj5Liv0t5AAIVBAACvM9BV9WweboNia0rHgQ'
    ]
}


@UserBot.on_message(filters.command(["sticker"], ".") & filters.me)
async def sticker_sender(bot: UserBot, message: Message):
    if len(message.command) > 1:
        set_to_send = message.command[1]

        if type(set_to_send) == str:
            set_to_send = int(set_to_send)

        stickers = SETS[set_to_send]

        for x in stickers:
            await bot.send_sticker(message.chat.id, x)


# @UserBot.on_message(filters.sticker & filters.me)
# async def sticker_sender(_, message: Message):
#     print(message.sticker.file_id)
