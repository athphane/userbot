from userbot import spotify
from spotipy import SpotifyException


async def now_playing():
    if not spotify:
        return "API details not set"

    current_track = spotify.currently_playing()
    return current_track


async def list_devices():
    if not spotify:
        return "API details not set"

    current_devices = spotify.devices()
    return current_devices


async def pause():
    if not spotify:
        return "API details not set"

    try:
        spotify.pause_playback()
        return True
    except SpotifyException:
        return False


async def play():
    if not spotify:
        return "API details not set"

    try:
        spotify.start_playback()
        return True
    except SpotifyException:
        return False
