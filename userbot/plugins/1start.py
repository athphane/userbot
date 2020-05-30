import asyncio
from datetime import datetime
from platform import python_version

from pyrogram import Filters, Message, __version__

from userbot import UserBot, START_TIME
from userbot.helpers.constants import First
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command("alive", ".") & Filters.me)
async def alive(bot: UserBot, message: Message):
    await message.edit(First.ALIVE)
    txt = (
        f"**{UserBot.__name__}** ```RUNNING```\n"
        f"-> Current Uptime: `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f"-> Python: `{python_version()}`\n"
        f"-> Pyrogram: `{__version__}`"
    )
    await message.edit(txt)


@UserBot.on_message(Filters.command("repo", ".") & Filters.me)
async def repo(bot: UserBot, message: Message):
    await message.edit("Click <a href=\"https://github.com/athphane/userbot\">here</a> to open Usebot's GitHub page.")


@UserBot.on_message(Filters.command("creator", ".") & Filters.me)
async def creator(bot: UserBot, message: Message):
    await message.edit(
        "I was created by my master <a href=\"https://github.com/athphane\">Athphane</a> on a rainy day."
    )


@UserBot.on_message(Filters.command(['uptime', 'up'], ".") & Filters.me)
async def uptime(bot: UserBot, message: Message):
    now = datetime.now()
    current_uptime = now - START_TIME
    await message.edit(
        f"Current Uptime\n"
        f"```{str(current_uptime).split('.')[0]}```"
    )


@UserBot.on_message(Filters.command("id", ".") & Filters.me)
async def get_id(bot: UserBot, message: Message):
    file_id = None

    if message.reply_to_message:
        rep = message.reply_to_message
        if rep.audio:
            file_id = rep.audio.file_id
        elif rep.document:
            file_id = rep.document.file_id
        elif rep.photo:
            file_id = rep.photo.file_id
        elif rep.sticker:
            file_id = rep.sticker.file_id
        elif rep.video:
            file_id = rep.video.file_id
        elif rep.animation:
            file_id = rep.animation.file_id
        elif rep.voice:
            file_id = rep.voice.file_id
        elif rep.video_note:
            file_id = rep.video_note.file_id
        elif rep.contact:
            file_id = rep.contact.file_id
        elif rep.location:
            file_id = rep.location.file_id
        elif rep.venue:
            file_id = rep.venue.file_id

    if not file_id:
        await message.edit("This chat's ID:\n`{}`".format(message.chat.id))
    else:
        await message.edit("File_ID:\n`{}`".format(file_id))


@UserBot.on_message(Filters.command("restart", '.') & Filters.me)
async def restart(bot: UserBot, message: Message):
    message.stop_propagation()
    await message.edit(f"Restarting {UserBot.__name__}.")
    await bot.send_message('me', f'#userbot_restart, {message.chat.id}, {message.message_id}')

    if 'p' in message.text and 'g' in message.text:
        asyncio.get_event_loop().create_task(bot.restart(git_update=True, pip=True))
    elif 'p' in message.text:
        asyncio.get_event_loop().create_task(bot.restart(pip=True))
    elif 'g' in message.text:
        asyncio.get_event_loop().create_task(bot.restart(git_update=True))
    else:
        asyncio.get_event_loop().create_task(bot.restart())


# Command help section
add_command_help(
    'start', [
        ['.alive', 'Check if the bot is alive or not.'],
        ['.repo', 'Display the repo of this userbot.'],
        ['.creator', 'Show the creator of this userbot.'],
        ['.id', 'Send id of what you replied to.'],
        ['.up `or` .uptime', 'Check bot\'s current uptime.']
    ]
)

add_command_help(
    'restart', [
        ['.restart', 'You are retarded if you do not know what this does.'],
        ['.restart g', 'Pull latest changes from git repo and restarts.'],
        ['.restart p', 'Installs pip requirements restarts.'],
        ['.restart gp', 'Pull latest changes from git repo, install pip requirements and restarts.'],
    ]
)
