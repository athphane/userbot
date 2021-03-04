from userbot import spotify


async def now_playing():
    if spotify:
        return "API details not set"

    current_track = spotify.currently_playing()
    return current_track


async def list_devices():
    if spotify:
        return "API details not set"

    current_devices = spotify.devices()
    return current_devices
