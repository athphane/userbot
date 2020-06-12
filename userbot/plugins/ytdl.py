# Thanks to @AvinashReddy3108 for this plugin
import asyncio
import os
import time

from pyrogram import Filters, Message
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)

from userbot import UserBot

"""
Audio and video downloader using Youtube-dl
.yta To Download in mp3 format
.ytv To Download in mp4 format
"""


@UserBot.on_message(Filters.command(['yta', 'ytv'], '.') & Filters.me)
async def download_video(bot: UserBot, message: Message):
    """ For .ytdl command, download media from YouTube and many other sites. """
    url = message.command[1]
    type = message.command[0]

    await message.edit("`Preparing to download...`")

    if type == "yta":
        opts = {
            'format': 'bestaudio',
            'addmetadata': True,
            'key': 'FFmpegMetadata',
            'writethumbnail': True,
            'prefer_ffmpeg': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': '%(id)s.mp3',
            'quiet': True,
            'logtostderr': False
        }
        video = False
        song = True

    elif type == "ytv":
        opts = {
            'format': 'best',
            'addmetadata': True,
            'key': 'FFmpegMetadata',
            'prefer_ffmpeg': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl': '%(id)s.mp4',
            'logtostderr': False,
            'quiet': True
        }
        song = False
        video = True

    try:
        await message.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await message.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await message.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await message.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a "
            "website.` "
        )
        return
    except MaxDownloadsReached:
        await message.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await message.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await message.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await message.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await message.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await message.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()

    if song:
        await asyncio.sleep(2)
        await message.edit(
            f"`Preparing to upload song:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*")
        await asyncio.sleep(2)
        await bot.send_audio(
            message.chat.id,
            f"{ytdl_data['id']}.mp3",
            duration=int(ytdl_data['duration']),
            title=str(ytdl_data['title']),
            performer=str(ytdl_data['uploader']),
        )
        os.remove(f"{ytdl_data['id']}.mp3")
        await message.delete()
    elif video:
        await asyncio.sleep(2)
        await message.edit(f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*")
        await asyncio.sleep(2)

        await bot.send_video(
            message.chat.id,
            f"{ytdl_data['id']}.mp4",
            caption=ytdl_data['title'],
        )
        os.remove(f"{ytdl_data['id']}.mp4")
        await message.delete()
