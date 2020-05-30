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
    id = master.commit.hexsha[:7]
    author = master.commit.author.name
    date_time = datetime.datetime.fromtimestamp(master.commit.committed_date)
    commit_msg = f"**Latest commit**:\n```{id}```\n\n**Commit Message**:\n```{commit.strip()}```\n\n**By**: ```{author}```\n\n**On**: ```{date_time}```"
    await message.edit(commit_msg)

# Command help section
add_command_help(
    'git', [
        ['.lastcommit | .lc', 'Gets the last commit message.'],
    ]
)
