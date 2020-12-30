import asyncio
from random import choice, randint

from pyrogram import filters
from pyrogram.types import Message
from userbot import UserBot


@UserBot.on_message(filters.command("scam", ".") & filters.me)
async def scam(_, message: Message):
    options = (
        "typing",
        "upload_photo",
        "record_video",
        "upload_video",
        "record_audio",
        "upload_audio",
        "upload_document",
        "find_location",
        "record_video_note",
        "upload_video_note",
        "choose_contact",
        "playing",
    )

    input_str = message.command

    if len(input_str) == 1:  # Let bot decide action and time
        scam_action = choice(options)
        scam_time = randint(30, 60)

    elif len(input_str) == 2:  # User decides time/action, bot decides the other.
        try:
            scam_action = str(input_str[1]).lower()
            scam_time = randint(30, 60)

        except ValueError:
            scam_action = choice(options)
            scam_time = int(input_str[1])

    elif len(input_str) == 3:  # User decides both action and time
        scam_action = str(input_str[1]).lower()
        scam_time = int(input_str[2])

    else:
        await message.edit("`Invalid Syntax !!`")
        return

    try:
        if scam_time > 0:
            chat_id = message.chat.id
            await message.delete()

            count = 0
            while count <= scam_time:
                await UserBot.send_chat_action(chat_id, scam_action)
                await asyncio.sleep(5)
                count += 5

    except Exception:
        return
