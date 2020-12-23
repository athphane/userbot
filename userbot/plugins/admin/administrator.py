import time

from pyrogram import filters
from pyrogram.types import Message, ChatPermissions

from pyrogram.errors import UserAdminInvalid

from userbot import UserBot
from userbot.helpers.PyroHelpers import GetUserMentionable
from userbot.helpers.adminHelpers import CheckAdmin, CheckReplyAdmin, RestrictFailed
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command("ban", ".") & filters.me)
async def ban_hammer(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            if message.command == ["ban", "24"]:
                await UserBot.kick_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    until_date=int(time.time() + 86400),
                )
                await message.edit(f"{mention} has been banned for 24hrs.")
            else:
                await UserBot.kick_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                )
                await message.edit(f"{mention} has been banned indefinitely.")
        except UserAdminInvalid:
            await RestrictFailed(message)


@UserBot.on_message(filters.command("unban", ".") & filters.me)
async def unban(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            await UserBot.unban_chat_member(
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
    can_send_stickers=False,
    can_send_animations=False,
    can_send_games=False,
    can_use_inline_bots=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@UserBot.on_message(filters.command(["mute", "mute 24"], ".") & filters.me)
async def mute_hammer(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            if message.command == ["mute", "24"]:
                await UserBot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    permissions=mute_permission,
                    until_date=int(time.time() + 86400),
                )
                await message.edit(f"{mention} has been muted for 24hrs.")
            else:
                await UserBot.restrict_chat_member(
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
    can_send_stickers=True,
    can_send_animations=True,
    can_send_games=True,
    can_use_inline_bots=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@UserBot.on_message(filters.command("unmute", ".") & filters.me)
async def unmute(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            await UserBot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                permissions=unmute_permissions,
            )
            await message.edit(f"{mention}, you may send messages here now.")
        except UserAdminInvalid:
            await RestrictFailed(message)


@UserBot.on_message(filters.command("kick", ".") & filters.me)
async def kick_user(_, message: Message):
    if await CheckReplyAdmin(message) is True and await CheckAdmin(message) is True:
        try:
            mention = GetUserMentionable(message.reply_to_message.from_user)
            await UserBot.kick_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
            )
            await message.edit(f"{mention}, Sayonara motherfucker.")
        except UserAdminInvalid:
            await RestrictFailed(message)


add_command_help(
    "ban",
    [
        [".ban", "Bans user indefinitely."],
        [".ban 24", "Bans user for 24hrs."],
        [".unban", "Unbans the user."],
        [".mute", "Mutes user indefinitely."],
        [".mute 24", "Bans user for 24hrs."],
        [".unmute", "Unmutes the user."],
        [".kick", "Kicks the user out of the group."],
    ],
)
