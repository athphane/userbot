import spotipy
import spotipy.util as util
from userbot import SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

redirect_uri = "http://localhost:8888/callback"
scope = 'user-read-currently-playing'


async def now_playing():
    if [x for x in (SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) if x is None]:
        return "API details not set"

    token = util.prompt_for_user_token(
        SPOTIFY_USERNAME, scope, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, redirect_uri)

    spotify = spotipy.Spotify(auth=token)

    current_track = spotify.currently_playing()
    return current_track
