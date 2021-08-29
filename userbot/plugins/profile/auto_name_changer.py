import asyncio
import json

from pyrogram import emoji, filters
from pyrogram.raw import functions
from pyrogram.types import Message

import userbot
from userbot import UserBot
from userbot.helpers import spotify

CHANGE_FLAG = False


def get_flag_status():
    return CHANGE_FLAG


@UserBot.on_message(filters.command(["enablesongbio"], ".") & filters.me)
async def enable_bio_changer(_, message: Message):
    global CHANGE_FLAG
    CHANGE_FLAG = True
    await message.edit("bio changer enabled.")
    await asyncio.sleep(3)
    await message.delete()


@UserBot.on_message(filters.command(["disablesongbio"], ".") & filters.me)
async def disable_bio_changer(_, message: Message):
    global CHANGE_FLAG
    CHANGE_FLAG = False
    await message.edit("bio changer disabled.")
    await asyncio.sleep(3)
    await message.delete()


async def change_bio(bot: UserBot):
    if get_flag_status():
        current_track = await spotify.now_playing()

        if not current_track:
            return

        if current_track == "API details not set":
            return

        print(json.dumps(current_track, indent=4, sort_keys=True))
        track = current_track['item']
        song = track['name']

        await bot.send(functions.account.UpdateProfile(
            about=f"{emoji.MUSICAL_NOTE}: {song}"
        ))


userbot.scheduler.add_job(change_bio, 'interval', seconds=60, misfire_grace_time=20, args=[userbot.client])
