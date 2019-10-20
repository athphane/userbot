from userbot import BOT, PM_PERMIT, PM_LIMIT
from pyrogram import Filters, Message
from pyrogram.errors import FloodWait
from userbot.plugins.help import add_command_help
from userbot.database.pmpermit import PmPermit
from time import sleep


UNAPPROVED_MSG = (
    "`Bleep blop! I'm a bot and this is an AUTOMATED MESSAGE..\n\n`"
    "`My master hasn't approved you to PM.`"
    "`Please wait for my master to look in, he mostly approves PMs.\n\n`"
    "`As far as I know, he doesn't usually approve retards though.`"
)


@BOT.on_message(Filters.private & ~Filters.me)
def incoming_pm(bot: BOT, message: Message):
    if PM_PERMIT:
        approved = PmPermit().check_if_approved(message.chat.id)
        warned = PmPermit().check_if_warned(message.chat.id)
        force_blocked = PmPermit().check_if_force_blocked(message.chat.id)

        if approved:
            return
        elif not approved and not warned:
            message.reply(UNAPPROVED_MSG)
            PmPermit().warn(message.chat.id)
            PmPermit().increment_retard_level(message.chat.id)
        elif not approved and warned and not force_blocked:
            if PmPermit().calculate_retard_level(message.chat.id) >= PM_LIMIT:
                message.reply("You have been blocked for being a retard.")

                BOT.block_user(message.chat.id)
                for dialog in BOT.iter_dialogs():
                    if dialog.chat.id == message.chat.id:
                        history = BOT.iter_history(message.chat.id, reverse=True)
                        for item in history:
                            try:
                                BOT.delete_messages(chat_id=message.chat.id, message_ids=item.message_id)
                                sleep(0.3)
                            except FloodWait as e:
                                sleep(e.x)
            else:
                PmPermit().increment_retard_level(message.chat.id)


@BOT.on_message(Filters.private & Filters.me)
def auto_approve_user_on_message(bot: BOT, message: Message):
    PmPermit().approve(message.chat.id)


@BOT.on_message(Filters.command('approve', '.') & Filters.me)
def approve(bot: BOT, message: Message):
    PmPermit().approve(message.chat.id)
    message.edit("You have been approved to PM me. Please continue on with your story.")
    sleep(3)
    message.delete()


@BOT.on_message(Filters.command('block', '.') & Filters.me)
def block(bot: BOT, message: Message):
    PmPermit().block_pm(message.chat.id)
    message.edit("`You have been blocked. Sad day for you init.`")
    BOT.block_user(message.chat.id)


if PM_PERMIT:
    add_command_help(
        'pmpermit',
        [
            ['.approve', "Approves the current chat to PM.\nUsage: `.approve`"],
            ['.block', "Blocks the current chat to PM.\nUsage: `.block`"],
        ]
    )