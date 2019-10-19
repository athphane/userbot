from time import sleep
from userbot.database.reminders import Reminders
from userbot import BOT
from pyrogram import Filters, Message
from pyrogram import Emoji

from userbot.plugins.help import add_command_help


@BOT.on_message(Filters.command('reminders', '.') & Filters.me)
def show_all_reminders(bot: BOT, message: Message):
    reminders = Reminders.get_all_reminders()
    if len(reminders) != 0:
        send_text = "**==== My Reminders ====** \n"
        for reminder in reminders:
            send_text = send_text + f"{reminder[0]} | **{reminder[1]}**\n"

        message.edit(send_text, disable_web_page_preview=True)
        sleep(20)
        message.delete()
    else:
        send_text = "** You do not have any reminders **"
        message.edit(send_text, disable_web_page_preview=True)
        sleep(5)
        message.delete()


@BOT.on_message(Filters.command("remind", ".") & Filters.me)
def remind(bot: BOT, message: Message):
    cmd = message.command
    remind_text = ""
    if len(cmd) > 1:
        remind_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        remind_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        message.edit(f"I need something to remind you about {Emoji.CRYING_FACE}")
        sleep(2)
        message.delete()
        return

    Reminders.add_reminder(remind_text)
    message.edit("```Reminder added```")
    sleep(2)
    message.delete()


@BOT.on_message(Filters.command("reminder", "!") & Filters.me)
def delete_remind(bot: BOT, message: Message):
    cmd = message.command
    reminder_id = ""
    if len(cmd) > 1:
        reminder_id = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        reminder_id = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        message.edit(f"I need the reminder ID to delete it {Emoji.CRYING_FACE}")
        sleep(2)
        message.delete()
        return

    if Reminders.find_reminder(reminder_id) is not None:
        Reminders.delete_reminder(reminder_id)
        message.edit("```Reminder deleted```")
        sleep(2)
        message.delete()
    else:
        message.edit(f"```Reminder {reminder_id} not found```")
        sleep(2)
        message.delete()


add_command_help(
    'reminders', [
        ['.reminders', 'Show all of your reminders.'],
        ['.remind', 'Add to reminders.\nUsage: reply to message or command args'],
        ['!reminder', 'Delete reminder from list.\nUsage: `!reminder code_from_.reminders`'],
    ]
)
