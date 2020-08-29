from time import sleep

from pyrogram import filters, emoji
from pyrogram.types import Message
from userbot import UserBot
from userbot.database.reminders import Reminders
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command('reminders', '.') & filters.me)
async def show_all_reminders(_, message: Message):
    reminders = Reminders().get_all_reminders()
    if len(reminders) != 0:
        send_text = "**==== My Reminders ====** \n"
        for reminder in reminders:
            send_text = send_text + f"{reminder[0]} | **{reminder[1]}**\n"

        await message.edit(send_text, disable_web_page_preview=True)
        sleep(20)
        await message.delete()
    else:
        send_text = "__You do not have any reminders__"
        await message.edit(send_text, disable_web_page_preview=True)
        sleep(5)
        await message.delete()


@UserBot.on_message(filters.command("remind", ".") & filters.me)
async def remind(_, message: Message):
    cmd = message.command
    remind_text = ""
    if len(cmd) > 1:
        remind_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        remind_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit(f"__I need something to remind you about {emoji.CRYING_FACE}__")
        sleep(2)
        await message.delete()
        return

    Reminders().add_reminder(remind_text)
    await message.edit("`Reminder added`")
    sleep(2)
    await message.delete()


@UserBot.on_message(filters.command("reminder", "!") & filters.me)
async def delete_reminder(_, message: Message):
    cmd = message.command
    reminder_id = ""
    if len(cmd) > 1:
        reminder_id = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        reminder_id = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit(f"I need the reminder ID to delete it {emoji.CRYING_FACE}")
        sleep(2)
        await message.delete()
        return

    if Reminders().find_reminder(reminder_id) is not None:
        Reminders().delete_reminder(reminder_id)
        await message.edit("```Reminder deleted```")
        sleep(2)
        await message.delete()
    else:
        await message.edit(f"```Reminder {reminder_id} not found```")
        sleep(2)
        await message.delete()


add_command_help(
    'reminders', [
        ['.reminders', 'Show all of your reminders.'],
        ['.remind', 'Add to reminders.\nUsage: reply to message or command args'],
        ['!reminder', 'Delete reminder from list.\nUsage: `!reminder code_from_.reminders`'],
    ]
)
