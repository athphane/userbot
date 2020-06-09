from datetime import datetime

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.helpers.spacex import get_latest
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['spacex', 'elon', 'ae12'], '.') & Filters.me)
async def nice(bot: UserBot, message: Message):
    await message.delete()

    data = await get_latest()

    dt = datetime.utcfromtimestamp(int(data['launch_date_unix'])).strftime('%d-%m-%Y %H:%M:%S')
    images = data['links']['flickr_images']

    txt = f"<b>Mission Name:</b> {data['mission_name']}\n" \
          f"<b>Flight No:</b> {data['flight_number']}\n" \
          f"<b>Rocket Name:</b> {data['rocket']['rocket_name']}\n" \
          f"<b>Launch Site:</b> {data['launch_site']['site_name_long']}\n" \
          f"<b>Reddit Campaign:</b> {data['links']['reddit_campaign']}\n" \
          f"<b>Video:</b> {data['links']['video_link']}\n"

    if images:
        for i, image in enumerate(images, start=1):
            txt += f"<b>Image {i}:</b> {image}\n"

    txt += f"<b>Details</b>: {data['details']}"

    if images:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=images[0],
            caption=txt,
            reply_to_message_id=ReplyCheck(message)
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=txt,
            disable_web_page_preview=True
        )

# Command help section
add_command_help(
    'spacex', [
        ['.spacex', 'Get the latest launch details']
    ]
)
