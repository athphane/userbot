import asyncio
from datetime import datetime
from pyrogram import Filters, Message
from pyrogram.client.methods.chats.get_chat_members import Filters as ChatMemberFilters

from userbot import UserBot
from userbot.plugins.help import add_command_help


async def CheckAdmin(bot: UserBot, message: Message):
    # Here lies the sanity checks
    admins = await bot.get_chat_members(message.chat.id, filter=ChatMemberFilters.ADMINISTRATORS)
    admin_ids = [user.user.id for user in admins]
    me = await bot.get_me()

    # If you are an admin
    if me.id in admin_ids:
        return True

    return False


@UserBot.on_message(Filters.command('purge', '.') & Filters.me)
async def purge_messages(bot: UserBot, message: Message):
    if message.chat.type in ['group', 'supergroup']:
        if not await CheckAdmin(bot, message):
            await message.edit("`Can't delete messages here. wew`")
            return

    start_t = datetime.now()
    message_ids = []
    deletion_count = 0
    if message.reply_to_message:
        for a_s_message_id in range(message.reply_to_message.message_id, message.message_id):
            message_ids.append(a_s_message_id)
            if len(message_ids) == 100:
                await bot.delete_messages(message.chat.id, message_ids, revoke=True)
                deletion_count += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await bot.delete_messages(message.chat.id, message_ids, revoke=True)
            deletion_count += len(message_ids)

    end_t = datetime.now()
    time_taken_ms = (end_t - start_t).seconds

    await message.edit(f"Purged {deletion_count} messages in {time_taken_ms} seconds")

    # RIP.
    await asyncio.sleep(3)
    await message.delete()


# Command help section
add_command_help(
    'admin', [
        ['.purge', 'Purge all messages up until the replied to message.']
    ]
)
