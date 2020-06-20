from time import sleep

from pyrogram import Message, User
from pyrogram.api import functions, types

from userbot import UserBot

from userbot.plugins.interval import IntervalHelper


async def CheckAdmin(bot: UserBot, message: Message):
    """Check if we are an admin."""

    admin = 'administrator'
    creator = 'creator'
    ranks = [admin, creator]

    SELF = await bot().get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id)

    if await SELF.status not in ranks:
        await message.edit("__I'm not Admin!__")
        sleep(2)
        await message.delete()

    else:
        if await SELF.status is not admin:
            return True
        elif await SELF.permissions.can_restrict_members:
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


async def Timer(message: Message):
    if len(message.command) > 1:
        secs = IntervalHelper(message.command[1])
        return int(str(time()).split(".")[0] + secs.to_secs()[0])
    else:
        return 0


async def TimerString(message: Message):
    secs = IntervalHelper(message.command[1])
    return f"{secs.to_secs()[1]} {secs.to_secs()[2]}"


async def RestrictFailed(message: Message):
    await message.edit(f"I can't {message.command[1]} this user.")
    sleep(2)
    await message.delete()
