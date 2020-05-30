import git
import asyncio
from html import escape
import os
import aiohttp
from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command('lastcommit', '.') & Filters.me)
async def last_commit(bot: UserBot, message: Message):
    repo = git.Repo(os.getcwd())
    master = repo.head.reference
    commit = master.commit.message.strip()
    id = master.commit.hexsha
    author = master.commit.author.name
    commit_msg = f"**Latest commit**:\n```{id}```\n\n**Commit Message**:\n```{commit.strip()}```\n\n**By**: ```{author}```"
    await message.edit(commit_msg)

# Command help section
add_command_help(
    'git', [
        ['.lastcommit', 'Gets the last commit message.'],
    ]
)
