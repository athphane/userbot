import asyncio

from pyrogram import Filters, Message
from pyrogram.api import functions

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['unread', 'un'], ".") & Filters.me)
async def mark_chat_unread(_, message: Message):
    await asyncio.gather(
        message.delete(),
        UserBot.send(
            functions.messages.MarkDialogUnread(
                peer=await UserBot.resolve_peer(message.chat.id), unread=True
            )
        )
    )

# Command help section
add_command_help(
    'chat', [
        ['.unread', 'Mark chat as unread.'],
    ]
)
