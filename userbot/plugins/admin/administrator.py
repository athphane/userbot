from time import time

from pyrogram import Filters, Message
from pyrogram.errors import UserAdminInvalid

from userbot import UserBot
from userbot.helpers.PyroHelpers import GetUserMentionable
from userbot.helpers.adminHelpers import (
    CheckAdmin, CheckReplyAdmin, Timer, TimerString, RestrictFailed
)


@UserBot.on_message(Filters.command("ban", prefixes='.') & Filters.me)
async def ban_hammer(bot: UserBot, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(bot, message) is True:
        try:
            mention = await GetUserMentionable(message.reply_to_message.from_user)
            await bot.kick_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                until_date=int(time.time() + 86400)
            )
            if len(message.command) > 1:
                await message.edit(f"{mention} has been banned for {until_date}.")
            else:
                await message.edit(f"{mention} has been banned indefinitely.")
        except UserAdminInvalid:
            await RestrictFailed(message)


@UserBot.on_message(Filters.command("unban", prefixes='.') & Filters.me)
async def unban(bot: UserBot, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(bot, message) is True:
        try:
            mention = await GetUserMentionable(message.reply_to_message.from_user)
            await bot.unban_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id
            )
            await message.edit(f"Congratulations {mention} you have been unbanned." 
                               "Follow the rules and be careful from now on.")
        except UserAdminInvalid:
            await message.edit("I can't unban this user.")


@UserBot.on_message(Filters.command("mute", prefixes='.') & Filters.me)
async def mute_hammer(bot: UserBot, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(bot, message) is True:
        try:
            mention = await GetUserMentionable(message.reply_to_message.from_user)
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                permissions=ChatPermissions(),
                until_date=int(time.time() + 86400)
            )
            if len(message.command) > 1:
                await message.edit(f"{mention} has been muted for {until_date}.")
            else:
                await message.edit(f"{mention} has been muted indefinitely.")
        except UserAdminInvalid:
            await RestrictFailed(message)


@UserBot.on_message(Filters.command("unmute", prefixes='.') & Filters.me)
async def unmute(bot: UserBot, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(bot, message) is True:
        try:
            mention = await GetUserMentionable(message.reply_to_message.from_user)
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                until_date=0,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True
            )
            await message.edit(f"{mention}, you may send messages here now.")
        except UserAdminInvalid:
            await RestrictFailed(message)


@UserBot.on_message(Filters.command("kick", prefixes='.') & Filters.me)
async def kick_user(bot: UserBot, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(bot, message) is True:
        try:
            mention = await GetUserMentionable(message.reply_to_message.from_user)
            await bot.kick_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
            )
            await bot.unban_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id
            )
            await message.edit(f"{mention}, Sayonara motherfucker.")
        except UserAdminInvalid:
            await RestrictFailed(message)
