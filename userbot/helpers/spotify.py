import spotipy
import spotipy.util as util
from userbot import USERNAME, CLIENT_ID, CLIENT_SECRET

redirect_uri = "http://localhost:8888/callback"
scope = 'user-read-currently-playing'

async def now_playing():
    token = util.prompt_for_user_token(
        USERNAME, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

    spotify = spotipy.Spotify(auth=token)

    current_track = spotify.currently_playing()
    return current_track
