# While it works completely fine, i have decided to comment it all out during the development phase. I personally am
# not happy how it works, especially the message deletion part. Maybe that is not supposed to be there
import asyncio

from pyrogram import Filters, Message

from userbot import UserBot, PM_PERMIT, PM_LIMIT
from userbot.database.pmpermit import PmPermit
from userbot.helpers.PyroHelpers import GetUserMentionable
from userbot.plugins.help import add_command_help

UNAPPROVED_MSG = (
    "`Bleep blop! I'm a bot and this is an AUTOMATED MESSAGE..\n\n`"
    "`My master hasn't approved you to PM.`"
    "`Please wait for my master to look in, he mostly approves PMs.\n\n`"
    "`As far as I know, he doesn't usually approve retards though.`"
)


def str2bool(thing):
    return thing.lower() in ['yes', 'true', '1', 1, 't']


if str2bool(PM_PERMIT):
    @UserBot.on_message(Filters.private & ~Filters.me, group=-1)
    async def incoming_pm(bot: UserBot, message: Message):
        if str2bool(PM_PERMIT):
            approved = PmPermit().check_if_approved(message.chat.id)
            warned = PmPermit().check_if_warned(message.chat.id)
            force_blocked = PmPermit().check_if_force_blocked(message.chat.id)

            if approved:
                return
            elif force_blocked:
                return
            elif not approved and not warned:
                await message.reply(UNAPPROVED_MSG)
                PmPermit().warn(message.chat.id)
                PmPermit().increment_retard_level(message.chat.id)
            elif not approved and warned and not force_blocked:
                if PmPermit().calculate_retard_level(message.chat.id) >= PM_LIMIT:
                    await message.reply("You have been blocked for being a retard.")
                    PmPermit().block_pm(message.chat.id)
                    await bot.block_user(message.chat.id)
                else:
                    PmPermit().increment_retard_level(message.chat.id)


    @UserBot.on_message(Filters.private & Filters.me, group=5)
    async def auto_approve_user_on_message(bot: UserBot, message: Message):
        if not PmPermit().check_if_approved(message.chat.id):
            PmPermit().approve(message.chat.id)
            user = await bot.get_users(message.chat.id)
            notify = await bot.send_message(message.chat.id, f"`Auto allowed {GetUserMentionable(user)} to PM...`")
            await asyncio.sleep(3)
            await notify.delete()


    @UserBot.on_message(Filters.private & Filters.command(['approve', 'allow'], '.') & Filters.me, group=3)
    async def approve(bot: UserBot, message: Message):
        PmPermit().approve(message.chat.id)
        await message.edit("You have been approved to PM me. Please continue on with your story.")
        await asyncio.sleep(3)
        await message.delete()


    @UserBot.on_message(Filters.private & Filters.command('block', '.') & Filters.me, group=3)
    async def block(bot: UserBot, message: Message):
        PmPermit().block_pm(message.chat.id)
        await message.edit("`You have been blocked. Sad day for you init.`")
        await bot.block_user(message.chat.id)
        message.stop_propagation()


    @UserBot.on_message(Filters.private & Filters.command('pmreset', '.') & Filters.me, group=3)
    async def pm_reset(bot: UserBot, message: Message):
        PmPermit().pm_reset(message.chat.id)
        await message.edit("`This chat has been reset. It's as if you have never spoken to each other...`")
        message.stop_propagation()


    add_command_help(
        'pmpermit',
        [
            ['.approve', "Approves the current chat to PM.\nUsage: `.approve`"],
            ['.block', "Blocks the current chat to PM.\nUsage: `.block`"],
            ['.pmreset', "Resets things as if you never met the other person."],
        ]
    )
