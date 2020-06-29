from asyncio import sleep
from random import random

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.me & Filters.command(["q"], '.'))
async def quotly(bot: UserBot, message: Message):
    if not message.reply_to_message:
        await message.edit("Reply to any users text message")
        return
    await message.edit("```Making a Quote```")
    await message.reply_to_message.forward("@QuotLyBot")
    is_sticker = False
    progress = 0
    while not is_sticker:
        try:
            msg = await bot.get_history("@QuotLyBot", 1)
            check = msg[0]["sticker"]["file_id"]
            is_sticker = True
        except:
            await sleep(0.5)
            progress += random.randint(0, 10)
            try:
                await message.edit("```Making a Quote```\nProcessing {}%".format(progress))
            except:
                await message.edit("ERROR SUUUU")
    await message.edit("```Complete !```")
    msg_id = msg[0]["message_id"]
    await bot.forward_messages(message.chat.id, "@QuotLyBot", msg_id)


# Command help section
add_command_help(
    'quotly', [
        ['.q | .quote', 'Make a quote with reply to message.'],
    ]
)
