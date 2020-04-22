import asyncio
from random import choice, randint
from userbot import UserBot
from pyrogram import Filters, Message


@UserBot.on_message(Filters.command('scam', '.') & Filters.me)
async def scam(bot: UserBot, message: Message):
    options = ('typing', 'upload_photo', 'record_video', 'upload_video', 'record_audio',
               'upload_audio', 'upload_document', 'find_location', 'record_video_note',
               'upload_video_note', 'choose_contact', 'playing')

    input_str = message.command[1]
    args = input_str.split()

    if len(args) == 0:  # Let bot decide action and time
        scam_action = choice(options)
        scam_time = randint(30, 60)

    elif len(args) == 1:  # User decides time/action, bot decides the other.
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(30, 60)

        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])

    elif len(args) == 2:  # User decides both action and time
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])

    else:
        await message.edit("`Invalid Syntax !!`")
        return

    try:
        if scam_time > 0:
            chat_id = message.chat.id
            await message.delete()

            count = 0
            while count <= scam_time:
                await bot.send_chat_action(chat_id, scam_action)
                await asyncio.sleep(5)
                count += 5

    except Exception:
        return
