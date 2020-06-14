import git
import datetime
import asyncio
from html import escape
import os
import aiohttp
from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['lastcommit', 'lc'], '.') & Filters.me)
async def last_commit(bot: UserBot, message: Message):
    repo = git.Repo(os.getcwd())
    master = repo.head.reference
    commit = master.commit.message.strip()
    id = master.commit.hexsha
    commit_link = f"<a href='https://github.com/pokurt/userbot/commit/{id}'>{id[:7]}</a>"
    author = master.commit.author.name
    date_time = datetime.datetime.fromtimestamp(master.commit.committed_date)
    commit_msg = f"**Latest commit**: {commit_link}\n\n**Commit Message**:\n```{commit.strip()}```\n\n**By**: `{author}`\n\n**On**: `{date_time}`"
    await message.edit(commit_msg, disable_web_page_preview=True)

# Command help section
add_command_help(
    'git', [
        ['.lastcommit | .lc', 'Gets the last commit message.'],
    ]
)
