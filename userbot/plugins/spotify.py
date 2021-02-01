from pyrogram import filters
from pyrogram.types import Message
from userbot import UserBot, ALLOWED_USERS
from userbot.plugins.help import add_command_help

from userbot.helpers import spotify


@UserBot.on_message(filters.command(["np", "now", "nowplaying"], ".") & (filters.me | filters.user(ALLOWED_USERS)))
async def now_playing(_, message: Message):
    current_track = await spotify.now_playing()
    if not current_track:
        await message.edit("I am not playing any music right now!")
        return
    track = current_track['item']
    artist = track['artist'][0]['name']
    song = track['name']
    link = current_track['context']['external_urls']['spotify']
    await message.edit(f"Currently Playing: <a href="{link}">{song}</a> by {artist}")
