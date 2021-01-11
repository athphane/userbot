# While it works completely fine, i have decided to comment it all out during the development phase. I personally am
# not happy how it works, especially the message deletion part. Maybe that is not supposed to be there


# PM_PERMIT, PM_LIMIT
from pyrogram import filters
from pyrogram.types import Message
from userbot import UserBot


# from pyrogram.errors import FloodWait
# from userbot.plugins.help import add_command_help
# from userbot.database.pmpermit import PmPermit
# from time import sleep
#
#


@UserBot.on_message(filters.command("pmpermit", ".") & filters.me)
async def pm_permit_enable(_, message: Message):
    await message.delete()


# UNAPPROVED_MSG = (
#     "`Bleep blop! I'm a bot and this is an AUTOMATED MESSAGE..\n\n`"
#     "`My master hasn't approved you to PM.`"
#     "`Please wait for my master to look in, he mostly approves PMs.\n\n`"
#     "`As far as I know, he doesn't usually approve retards though.`"
# )
#
#
# @UserBot.on_message(filters.private & ~Filters.me)
# async def incoming_pm(_, message: Message):
#     if PM_PERMIT:
#         approved = PmPermit().check_if_approved(message.chat.id)
#         warned = PmPermit().check_if_warned(message.chat.id)
#         force_blocked = PmPermit().check_if_force_blocked(message.chat.id)
#
#         if approved:
#             return
#         elif not approved and not warned:
#             await message.reply(UNAPPROVED_MSG)
#             PmPermit().warn(message.chat.id)
#             PmPermit().increment_retard_level(message.chat.id)
#         elif not approved and warned and not force_blocked:
#             if PmPermit().calculate_retard_level(message.chat.id) >= PM_LIMIT:
#                 await message.reply("You have been blocked for being a retard.")
#                 dialogs = [x async for x in bot.iter_dialogs()]
#                 for dialog in dialogs:
#                     if dialog.chat.id == message.chat.id:
#                         await UserBot.block_user(message.chat.id)
#                         history = [x async for x in bot.iter_history(message.chat.id, reverse=True)]
#                         message_ids = [x.message_id for x in history]
#                         for item in history:
#                             try:
#                                 await UserBot.delete_messages(chat_id=message.chat.id, message_ids=[item.message_id])
#                                 sleep(0.3)
#                             except FloodWait as e:
#                                 sleep(e.x)
#             else:
#                 PmPermit().increment_retard_level(message.chat.id)
#
#
# @UserBot.on_message(filters.private & filters.me)
# async def auto_approve_user_on_message(_, message: Message):
#     PmPermit().approve(message.chat.id)
#
#
# @UserBot.on_message(filters.command('approve', '.') & filters.me)
# async def approve(_, message: Message):
#     PmPermit().approve(message.chat.id)
#     await message.edit("You have been approved to PM me. Please continue on with your story.")
#     sleep(3)
#     await message.delete()
#
#
# @UserBot.on_message(filters.command('block', '.') & filters.me)
# async def block(_, message: Message):
#     PmPermit().block_pm(message.chat.id)
#     await message.edit("`You have been blocked. Sad day for you init.`")
#     await UserBot().block_user(message.chat.id)
#
#
# if PM_PERMIT:
#     add_command_help(
#         'pmpermit',
#         [
#             ['.approve', "Approves the current chat to PM.\nUsage: `.approve`"],
#             ['.block', "Blocks the current chat to PM.\nUsage: `.block`"],
#         ]
#     )

# Command help section
# add_command_help(
#     'metrics', [
#         ['.wordcount', 'Finds the 50 most used words in the last 2000 messages in a group or private chat. Use in '
#                        'chat you want to find the metric in.'],
#     ]
# )
