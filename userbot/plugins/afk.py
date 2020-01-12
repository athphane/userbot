from userbot import UserBot
from userbot.plugins.help import add_command_help
from pyrogram import Filters, Message

AFK = False
AFK_REASON = ''


@UserBot.on_message(Filters.mentioned | Filters.private & Filters.text & ~Filters.me, group=3)
async def reply_to_mentioned(bot: UserBot, message: Message):
    if AFK:
        text = (
            f"```Beep boop. This is an automated message.```\n"
            f"I am not available right now.\n"
            f"Here's why: ```{AFK_REASON.upper()}```\n"
            f"See you after I'm done doing whatever I'm doing."
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_to_message_id=message.message_id
        )


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
    global AFK, AFK_REASON
    AFK = False
    AFK_REASON = ''
    await message.delete()


@UserBot.on_message(Filters.me & Filters.private | Filters.group, group=3)
async def back_online(bot: UserBot, message: Message):
    global AFK, AFK_REASON
    if AFK:
        AFK = False
        AFK_REASON = ''


add_command_help(
    'afk', [
        ['.afk', 'Activates AFK mode with reason as anything after .afk'],
        ['!afk', 'Deactivates AFK mode. Replying to ANY private chat or group deactivates it too']
    ]
)
