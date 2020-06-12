from time import sleep

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import GetFromUserID, GetChatID
from userbot.plugins.help import add_command_help

AFK = False
AFK_REASON = ''
USERS = {}
GROUPS = {}


@UserBot.on_message(Filters.group & Filters.mentioned & ~Filters.me, group=3)
async def afk_group(bot: UserBot, message: Message):
    if AFK:
        if GetChatID(message) not in GROUPS:
            text = (
                f"```Beep boop. This is an automated message.```\n"
                f"I am not available right now.\n"
                f"Here's why: ```{AFK_REASON.upper()}```\n"
                f"See you after I'm done doing whatever I'm doing."
            )
            await bot.send_message(
                chat_id=GetChatID(message),
                text=text,
                reply_to_message_id=message.message_id
            )
            GROUPS[GetChatID(message)] = 1
            return
        elif GetChatID(message) in GROUPS:
            if GROUPS[GetChatID(message)] == 50:
                text = (
                    f"```This is an automated message```\n"
                    f"This is the 10th time I've told you I'm AFK right now..\n"
                    f"I'll get to you when I get to you.\n"
                    f"No more auto messages for you"
                )
                await bot.send_message(
                    chat_id=GetChatID(message),
                    text=text,
                    reply_to_message_id=message.message_id
                )
            elif GROUPS[GetChatID(message)] > 50:
                return
            elif GROUPS[GetChatID(message)] % 5 == 0:
                text = (
                    f"Hey I'm still not back yet.\n"
                    f"Still busy with ```{AFK_REASON.upper()}```\n"
                    f"Try pinging a bit later."
                )
                await bot.send_message(
                    chat_id=GetChatID(message),
                    text=text,
                    reply_to_message_id=message.message_id
                )

        GROUPS[GetChatID(message)] += 1


@UserBot.on_message(Filters.private & ~Filters.me, group=3)
async def afk_private(bot: UserBot, message: Message):
    if AFK:
        if GetFromUserID(message) not in USERS:
            text = (
                f"```Beep boop. This is an automated message.```\n"
                f"I am not available right now.\n"
                f"Here's why: ```{AFK_REASON.upper()}```\n"
                f"See you after I'm done doing whatever I'm doing."
            )
            await bot.send_message(
                chat_id=GetFromUserID(message),
                text=text,
                reply_to_message_id=message.message_id
            )
            USERS[GetFromUserID(message)] = 1
            return
        elif GetFromUserID(message) in USERS:
            if USERS[GetFromUserID(message)] == 50:
                text = (
                    f"```This is an automated message```\n"
                    f"This is the 10th time I've told you I'm AFK right now..\n"
                    f"I'll get to you when I get to you.\n"
                    f"No more auto messages for you"
                )
                await bot.send_message(
                    chat_id=GetFromUserID(message),
                    text=text,
                    reply_to_message_id=message.message_id
                )
            elif USERS[GetFromUserID(message)] > 50:
                return
            elif USERS[GetFromUserID(message)] % 5 == 0:
                text = (
                    f"Hey I'm still not back yet.\n"
                    f"Still busy with ```{AFK_REASON.upper()}```\n"
                    f"Try pinging a bit later."
                )
                await bot.send_message(
                    chat_id=GetFromUserID(message),
                    text=text,
                    reply_to_message_id=message.message_id
                )

        USERS[GetFromUserID(message)] += 1


@UserBot.on_message(Filters.command("afk", ".") & Filters.me, group=3)
async def afk_set(bot: UserBot, message: Message):
    global AFK_REASON, AFK
    cmd = message.command
    afk_text = ''

    if len(cmd) > 1:
        afk_text = " ".join(cmd[1:])

    if isinstance(afk_text, str):
        AFK_REASON = afk_text

    AFK = True

    await message.delete()


@UserBot.on_message(Filters.command("afk", "!") & Filters.me, group=3)
async def afk_unset(bot: UserBot, message: Message):
    global AFK, AFK_REASON, USERS, GROUPS

    if AFK:
        await message.edit(f"While you were away, you received {sum(USERS.values()) + sum(GROUPS.values())} messages "
                           f"from {len(USERS) + len(GROUPS)} chats")
        AFK = False
        AFK_REASON = ''
        USERS = {}
        GROUPS = {}
        sleep(5)

    await message.delete()

@UserBot.on_message(Filters.me, group=3)
async def auto_afk_unset(bot: UserBot, message: Message):
    global AFK, AFK_REASON, USERS, GROUPS

    if AFK:
        reply = await message.reply(f"While you were away, you received {sum(USERS.values()) + sum(GROUPS.values())} messages "
                           f"from {len(USERS) + len(GROUPS)} chats")
        AFK = False
        AFK_REASON = ''
        USERS = {}
        GROUPS = {}
        sleep(5)

        await reply.delete()

 
add_command_help(
    'afk', [
        ['.afk', 'Activates AFK mode with reason as anything after .afk\nUsage: ```.afk <reason>```'],
        ['!afk', 'Deactivates AFK mode.']
    ]
)
