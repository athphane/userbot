from userbot import UserBot
from pyrogram import Filters, Message
from userbot.helpers.constants import First
from userbot.plugins.help import add_command_help
import asyncio


@UserBot.on_message(Filters.command("alive", ".") & Filters.me)
async def alive(bot: UserBot, message: Message):
    await message.edit(First.ALIVE)


@UserBot.on_message(Filters.command("repo", ".") & Filters.me)
async def repo(bot: UserBot, message: Message):
    await message.edit("Click <a href=\"https://github.com/athphane/userbot\">here</a> to open Usebot's GitHub page.")


@UserBot.on_message(Filters.command("creator", ".") & Filters.me)
async def creator(bot: UserBot, message: Message):
    await message.edit(
        "I was created by my master <a href=\"https://github.com/athphane\">Athphane</a> on a rainy day."
    )


@UserBot.on_message(Filters.command("id", ".") & Filters.me)
async def get_id(bot: UserBot, message: Message):
    out_str = f"💁 Current Chat ID: `{message.chat.id}`"

    if message.reply_to_message:
        out_str += f"`{message.reply_to_message.from_user.id}`"
        file_id = None

        if message.reply_to_message.media:
            if message.reply_to_message.audio:
                file_id = message.reply_to_message.audio.file_id

            elif message.reply_to_message.document:
                file_id = message.reply_to_message.document.file_id

            elif message.reply_to_message.photo:
                file_id = message.reply_to_message.photo.file_id

            elif message.reply_to_message.sticker:
                file_id = message.reply_to_message.sticker.file_id

            elif message.reply_to_message.voice:
                file_id = message.reply_to_message.voice.file_id

            elif message.reply_to_message.video_note:
                file_id = message.reply_to_message.video_note.file_id

            elif message.reply_to_message.video:
                file_id = message.reply_to_message.video.file_id

            if file_id is not None:
                out_str += f"`{file_id}`"

    await message.edit(out_str)


@UserBot.on_message(Filters.command("restart", '.') & Filters.me)
async def restart(bot: UserBot, message: Message):
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
    'alive', [['.alive', 'Check if the bot is alive or not.']]
)

add_command_help(
    'repo', [['.repo', 'Display the repo of this userbot.']]
)

add_command_help(
    'creator', [['.creator', 'Show the creator of this userbot.']]
)

add_command_help(
    'id', [['.id', 'Send id of what you replied to.']]
)

add_command_help(
    'restart', [
        ['.restart', 'You are retarded if you do not know what this does.'],
        ['.restart g', 'Pull latest changes from git repo and restarts.'],
        ['.restart p', 'Installs pip requirements restarts.'],
        ['.restart gp', 'Pull latest changes from git repo, install pip requirements and restarts.'],
    ]
)