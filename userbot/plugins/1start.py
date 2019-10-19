from userbot import BOT
from pyrogram import Filters, Message
from userbot.helpers.constants import First
from userbot.plugins.help import add_command_help


@BOT.on_message(Filters.command("alive", ".") & Filters.me)
def alive(bot: BOT, message: Message):
    message.edit(First.ALIVE)


@BOT.on_message(Filters.command("repo", ".") & Filters.me)
def repo(bot: BOT, message: Message):
    message.edit("https://github.com/athphane/userbot", disable_web_page_preview=True)


# Command help section
add_command_help(
    'alive', [['.alive', 'Check if the bot is alive or not.']]
)

add_command_help(
    'repo', [['.repo', 'Display the repo of this userbot.']]
)
