import asyncio
from pyrogram import enums, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import ChatPhoto, LinkPreviewOptions, Message, ReplyParameters, User

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help

WHOIS = (
    '**WHO IS "{full_name}"?**\n'
    "[Link to profile](tg://user?id={user_id})\n"
    "════════════════\n"
    "UserID: `{user_id}`\n"
    "First Name: `{first_name}`\n"
    "Last Name: `{last_name}`\n"
    "Username: `{username}`\n"
    "Last Online: `{last_online}`\n"
    "Common Groups: `{common_groups}`\n"
    "════════════════\n"
    "Bio:\n{bio}"
)

WHOIS_PIC = (
    '**WHO IS "{full_name}"?**\n'
    "[Link to profile](tg://user?id={user_id})\n"
    "════════════════\n"
    "UserID: `{user_id}`\n"
    "First Name: `{first_name}`\n"
    "Last Name: `{last_name}`\n"
    "Username: `{username}`\n"
    "Last Online: `{last_online}`\n"
    "Common Groups: `{common_groups}`\n"
    "════════════════\n"
    "Profile Pics: `{profile_pics}`\n"
    "Last Updated: `{profile_pic_update}`\n"
    "════════════════\n"
    "Bio:\n{bio}"
)


def LastOnline(user: User) -> str:
    """Format Kurigram's user status and datetime fields."""
    if user.is_bot:
        return ""
    elif user.status == enums.UserStatus.RECENTLY:
        return "Recently"
    elif user.status == enums.UserStatus.LAST_WEEK:
        return "Within the last week"
    elif user.status == enums.UserStatus.LAST_MONTH:
        return "Within the last month"
    elif user.status == enums.UserStatus.LONG_AGO:
        return "A long time ago :("
    elif user.status == enums.UserStatus.ONLINE:
        return "Currently Online"
    elif user.status == enums.UserStatus.OFFLINE and user.last_online_date:
        return user.last_online_date.strftime("%a, %d %b %Y, %H:%M:%S")
    return "Unknown"


async def GetCommon(bot: UserBot, get_user):
    return await bot.get_common_chats(get_user)


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


def ProfilePicUpdate(user_pic: list[ChatPhoto]) -> str:
    """Format the date attached to a Kurigram chat photo."""
    date = user_pic[0].added_date
    return date.strftime("%d.%m.%Y, %H:%M:%S") if date else "Unknown"


@UserBot.on_message(filters.command("whois", [".", ""]) & filters.me)
async def who_is(bot: UserBot, message: Message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif message.reply_to_message and len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await bot.get_users(get_user)
    except PeerIdInvalid:
        await message.edit("I don't know that User.")
        await asyncio.sleep(2)
        await message.delete()
        return

    user_details = await bot.get_chat(get_user)
    bio = user_details.bio
    user_pic = [photo async for photo in bot.get_chat_photos(user.id, limit=1)]
    pic_count = await bot.get_chat_photos_count(user.id)
    common = await GetCommon(bot, user.id)

    if not user_pic:
        await message.edit(
            WHOIS.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                common_groups=len(common),
                bio=bio if bio else "`No bio set up.`",
            ),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
    else:
        await bot.send_photo(
            message.chat.id,
            user_pic[0].big_file_id,
            caption=WHOIS_PIC.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                profile_pics=pic_count,
                common_groups=len(common),
                bio=bio if bio else "`No bio set up.`",
                profile_pic_update=ProfilePicUpdate(user_pic),
            ),
            reply_parameters=ReplyParameters(message_id=ReplyCheck(message)),
        )

        await message.delete()


add_command_help(
    "whois",
    [
        [
            ".whois",
            "Finds out who the person is. Reply to message sent by the person"
            "you want information from and send the command. Without the dot also works.",
        ]
    ],
)
