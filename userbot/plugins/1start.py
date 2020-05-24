from userbot import UserBot
from pyrogram import Filters, Message
from userbot.helpers.constants import First
from userbot.plugins.help import add_command_help


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
    file_id = None
    user_id = None

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
        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        await message.edit(user_id)
    elif file_id:
        await message.edit(file_id)
    else:
        await message.edit("This chat's ID:\n`{}`".format(message.chat.id))

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
