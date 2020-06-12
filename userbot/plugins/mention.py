import asyncio
from functools import partial

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

mention = partial(
    "<a href='tg://user?id={}'>{}</a>".format
)

hmention = partial(
    "<a href='tg://user?id={}'>\u200B</a>{}".format
)


@UserBot.on_message(Filters.command("mention", ".") & Filters.me)
async def mention_user(bot: UserBot, message: Message):
    if len(message.command) < 3:
        await message.edit("Incorrect format\nExample: .mention @Athfan CTO")
        await asyncio.sleep(3)
        await message.delete()
        return
    try:
        user = await bot.get_users(message.command[1])
    except Exception:
        await message.edit("User not found")
        await asyncio.sleep(3)
        await message.delete()
        return

    _mention = mention(user.id, ' '.join(message.command[2:]))
    await message.edit(_mention)


@UserBot.on_message(Filters.command("hmention", ".") & Filters.me)
async def hidden_mention(bot: UserBot, message: Message):
    if len(message.command) < 3:
        await message.edit("Incorrect format\nExample: .hmention @Athfan")
        await asyncio.sleep(3)
        await message.delete()
        return
    try:
        user = await bot.get_users(message.command[1])
    except Exception:
        await message.edit("User not found")
        await asyncio.sleep(3)
        await message.delete()
        return

    _hmention = hmention(user.id, ' '.join(message.command[2:]))
    await message.edit(_hmention)


# Command help section
add_command_help(
    'mention', [
        ['.mention', 'Mention a user with a different name\nExample: `.mention @Athfan CTO`'],
        ['.hmention', 'Mention a user with a hidden text\nExample: `.hmention @Athfan`']
    ]
)
