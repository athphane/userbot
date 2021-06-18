import asyncio
import random
from asyncio import sleep

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.me & filters.command(["q"], '.'))
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
            print(msg)
            is_sticker = True
        except:
            await sleep(1)

            progress += random.randint(0, 5)

            if progress > 100:
                await message.edit('There was a long running error')
                return

            try:
                await message.edit("```Making a Quote\nProcessing {}%```".format(progress))
            except:
                await message.edit("ERROR")

    if msg_id := msg[0]['message_id']:
        await asyncio.gather(
            message.delete(),
            bot.forward_messages(message.chat.id, "@QuotLyBot", msg_id)
        )


# Command help section
add_command_help(
    'quotly', [
        ['.q | .quote', 'Make a quote with reply to message.'],
    ]
)
