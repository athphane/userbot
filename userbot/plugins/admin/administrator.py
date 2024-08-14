import time

from pyrogram import filters
from pyrogram.errors import UserAdminInvalid
from pyrogram.types import ChatPermissions, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import GetUserMentionable
from userbot.helpers.adminHelpers import CheckAdmin, CheckReplyAdmin, RestrictFailed
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command('ban', '.') & filters.me)
async def ban_hammer(bot: UserBot, message: Message):
    duration = int(message.command[1]) if len(message.command) > 1 else False

    if await CheckReplyAdmin(message) and await CheckAdmin(message):
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            if duration:
                await bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    until_date=int(time.time() + (duration * 3600)),
                )
                await message.edit(f"{mention} has been banned for {duration} Hours.")
            else:
                await bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                )
                await message.edit(f"{mention} has been banned indefinitely.")
        except UserAdminInvalid:
            await RestrictFailed(message)


@UserBot.on_message(filters.command("unban", ".") & filters.me)
async def unban(bot: UserBot, message: Message):
    if await CheckReplyAdmin(message) and await CheckAdmin(message):
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)

            await bot.unban_chat_member(
                chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id
            )

            await message.edit(
                f"Congratulations {mention} you have been unbanned."
                " Follow the rules and be careful from now on."
            )
        except UserAdminInvalid:
            await message.edit("I can't unban this user.")


# Mute Permissions
mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@UserBot.on_message(filters.command('mute', '.') & filters.me)
async def mute_hammer(bot: UserBot, message: Message):
    duration = int(message.command[1]) if len(message.command) > 1 else False

    if await CheckReplyAdmin(message) and await CheckAdmin(message):
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            if duration:
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    permissions=mute_permission,
                    until_date=int(time.time() + (duration * 3600)),
                )
                await message.edit(f"{mention} has been muted for {duration} Hours.")
            else:
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    permissions=mute_permission,
                )
                await message.edit(f"{mention} has been muted indefinitely.")
        except UserAdminInvalid:
            await RestrictFailed(message)


# Unmute permissions
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@UserBot.on_message(filters.command("unmute", ".") & filters.me)
async def unmute(bot: UserBot, message: Message):
    if await CheckReplyAdmin(message) and await CheckAdmin(message):
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)

            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                permissions=unmute_permissions,
            )

            await message.edit(f"{mention}, you may send messages here now.")
        except UserAdminInvalid:
            await RestrictFailed(message)


@UserBot.on_message(filters.command("kick", ".") & filters.me)
async def kick_user(bot: UserBot, message: Message):
    if await CheckReplyAdmin(message) and await CheckAdmin(message):
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)

            await bot.ban_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                until_date=int(time.time() + (int(time.time()) * 3600)),
            )

            await message.edit(f"Goodbye, {mention}.")
        except UserAdminInvalid:
            await RestrictFailed(message)


add_command_help(
    "ban",
    [
        [".ban", "Bans user for specified hours or indefinitely."],
        [".unban", "Unbans the user."],
        [".mute", "Bans user for specified hours or indefinitely."],
        [".unmute", "Unmutes the user."],
        [".kick", "Kicks the user out of the group."],
    ],
)
