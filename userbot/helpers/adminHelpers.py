from time import sleep

from pyrogram import Message, User
from pyrogram.api import functions, types

from userbot import UserBot

from userbot.plugins.interval import IntervalHelper


def CheckAdmin(message: Message):
    """Check if we are an admin."""

    admin = 'administrator'
    creator = 'creator'
    ranks = [admin, creator]

    SELF = UserBot.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id)

    if SELF.status not in ranks:
        message.edit("__I'm not Admin!__")
        sleep(2)
        message.delete()

    else:
        if SELF.status is not admin:
            return True
        elif SELF.permissions.can_restrict_members:
            return True
        else:
            message.edit("__No Permissions to restrict Members__")
            sleep(2)
            message.delete()


def CheckReplyAdmin(message: Message):
    """Check if the message is a reply to another user."""
    if not message.reply_to_message:
        message.edit(f"`?{message.command[0]}` needs to be a reply")
        sleep(2)
        message.delete()
    elif message.reply_to_message.from_user.is_self:
        message.edit(f"I can't {message.command[0]} myself.")
        sleep(2)
        message.delete()
    else:
        return True


def Timer(message: Message):
    if len(message.command) > 1:
        secs = IntervalHelper(message.command[1])
        return int(str(time()).split(".")[0] + secs.to_secs()[0])
    else:
        return 0


def TimerString(message: Message):
    secs = IntervalHelper(message.command[1])
    return f"{secs.to_secs()[1]} {secs.to_secs()[2]}"


def RestrictFailed(message: Message):
    message.edit(f"I can't {message.command[1]} this user.")
    sleep(2)
    message.delete()