from datetime import datetime

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.helpers.spacex import get_latest, get_next
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['spacex', 'elon', 'ae12'], '.') & Filters.me)
async def spacex(bot: UserBot, message: Message):
    await message.delete()

    data = await get_latest()

    dt = datetime.utcfromtimestamp(int(data['launch_date_unix'])).strftime('%d-%m-%Y %H:%M:%S')
    images = data['links']['flickr_images']

    txt = f"<b>Mission Name:</b> {data['mission_name']}\n" \
          f"<b>Flight No:</b> {data['flight_number']}\n" \
          f"<b>Rocket Name:</b> {data['rocket']['rocket_name']}\n" \
          f"<b>Launch Site:</b> {data['launch_site']['site_name']}\n" \
          f"<b>Launch Date:</b> {dt}\n\n" \
          f"<b>Links:</b>\n" \
          f"<a href='{data['links']['reddit_campaign']}'>Reddit</a>, " \
          f"<a href='{data['links']['video_link']}'>YouTube</a>"

    if images:
        for i, image in enumerate(images, start=1):
            txt += f", <a href='{image}'>Flicker {i}</a>"

    txt += f"\n\n{data['details']}"

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


@UserBot.on_message(Filters.command(['nspacex', 'nextlaunch'], '.') & Filters.me)
async def next_launch(bot: UserBot, message: Message):
    await message.delete()

    data = await get_next()

    dt = datetime.utcfromtimestamp(int(data['launch_date_unix'])).strftime('%d-%m-%Y %H:%M:%S')

    txt = "<u><b>NEXT SPACEX LAUNCH</b></u>\n" \
          f"<b>Mission Name:</b> {data['mission_name']}\n" \
          f"<b>Flight No:</b> {data['flight_number']}\n" \
          f"<b>Rocket Name:</b> {data['rocket']['rocket_name']}\n" \
          f"<b>Launch Site:</b> {data['launch_site']['site_name']}\n" \
          f"<b>Launch Date:</b> {dt}" \
          f"\n\n{data['details']}"

    await bot.send_message(
        chat_id=message.chat.id,
        text=txt,
        disable_web_page_preview=True
    )


# Command help section
add_command_help(
    'spacex', [
        ['.spacex', 'Get the latest launch details'],
        ['.nspacex', 'Get the next launch details']
    ]
)
