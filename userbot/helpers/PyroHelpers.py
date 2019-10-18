from time import sleep
from datetime import datetime
from pyrogram import Message, User
from pyrogram.api import functions
from userbot import BOT


async def CheckAdmin(message: Message):
    """Check if we are admin."""

    admin = 'administrator'
    creator = 'creator'
    ranks = [admin, creator]

    SELF = await BOT.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id)

    if SELF.status not in ranks:
        await message.edit("__I'm not Admin!__")
        sleep(2)
        await message.delete()

    else:
        if SELF.status is not admin:
            return True
        elif SELF.permissions.can_restrict_members:
            return True
        else:
            await message.edit("__No Permissions to restrict Members__")
            sleep(2)
            await message.delete()


async def CheckReplyAdmin(message: Message):
    """Check if the message is a reply to another user."""
    if not message.reply_to_message:
        await message.edit(f"`?{message.command[0]}` needs to be a reply")
        sleep(2)
        await message.delete()
    elif message.reply_to_message.from_user.is_self:
        await message.edit(f"I can't {message.command[0]} myself.")
        sleep(2)
        await message.delete()
    else:
        return True


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


def LastOnline(user: User):
    if user.status.recently:
        return "Recently"
    elif user.status.within_week:
        return "Within the last week"
    elif user.status.within_month:
        return "Within the last month"
    elif user.status.long_time_ago:
        return "A long time ago :("
    elif user.status.online:
        return "Currently Online"
    elif user.status.offline:
        return datetime.fromtimestamp(user.status.date).strftime("%a, %d %b %Y, %H:%M:%S")


def SpeedConvert(size):
    power = 2 ** 10
    zero = 0
    units = {
        0: '',
        1: 'Kbit/s',
        2: 'Mbit/s',
        3: 'Gbit/s',
        4: 'Tbit/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


def GetChatID(message: Message):
    """ Get the chat id of the incoming message."""
    return message.chat.id


def GetUserMentionable(user: User):
    """ Get mentionable text of a user."""
    if user.username:
        username = "@{}".format(user.username)
    else:
        if user.last_name:
            name_string = "{} {}".format(user.first_name, user.last_name)
        else:
            name_string = "{}".format(user.first_name)

        username = "<a href='tg://user?id={}'>{}</a>".format(user.id, name_string)

    return username
