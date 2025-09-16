from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.database.ignore import ignore_db


@UserBot.on_message(filters.private & filters.command("ignore", '.'))
async def ignore_command(client: UserBot, message: Message):
    if not message.from_user:
        return
    user_id = message.chat.id
    if not ignore_db.is_ignored(user_id):
        ignore_db.ignore_user(user_id)
        await message.chat.archive()
        await message.reply_text("This chat has been ignored until further notice")
    else:
        await message.reply_text("This chat is already ignored.")


@UserBot.on_message(filters.private & filters.command("unignore", '.'))
async def unignore_command(client: UserBot, message: Message):
    if not message.from_user:
        return
    user_id = message.chat.id
    if ignore_db.is_ignored(user_id):
        ignore_db.unignore_user(user_id)
        await message.reply_text("This chat has been unignored.")
    else:
        await message.reply_text("This chat is not ignored.")


@UserBot.on_message(filters.private)
async def handle_ignored_message(client: Client, message: Message):
    if not message.from_user:
        return
    user_id = message.from_user.id
    if ignore_db.is_ignored(user_id):
        await client.read_chat_history(message.chat.id)
        last_message_time = ignore_db.get_last_message_time(user_id)
        if last_message_time is None or datetime.now() - last_message_time > timedelta(hours=1):
            await message.reply_text("This chat has been ignored and is not monitored by user")
            ignore_db.set_last_message_time(user_id)
    else:
        await message.continue_propagation()
