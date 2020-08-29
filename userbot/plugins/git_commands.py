import asyncio
import datetime
import os
from asyncio import sleep
from glob import iglob
from random import randint

import aiofiles
import git
from pyrogram import filters
from pyrogram.types import Message
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.helpers.aiohttp_helper import AioHttp
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command(['lastcommit', 'lc'], '.') & filters.me)
async def last_commit(_, message: Message):
    repo = git.Repo(os.getcwd())
    master = repo.head.reference
    commit = master.commit.message.strip()
    commit_id = master.commit.hexsha
    commit_link = f"<a href='https://github.com/athphane/userbot/commit/{commit_id}'>{commit_id[:7]}</a>"
    author = master.commit.author.name
    date_time = datetime.datetime.fromtimestamp(master.commit.committed_date)
    commit_msg = f"**Latest commit**: {commit_link}\n\n**Commit Message**:\n```{commit.strip()}```\n\n" \
                 f"**By**: `{author}`\n\n**On**: `{date_time}`"
    await message.edit(commit_msg, disable_web_page_preview=True)


@UserBot.on_message(filters.command(['ggraph', 'commitgraph'], '.') & filters.me)
async def commit_graph(_, message: Message):
    if len(message.command) < 2:
        await message.edit("Please provide a github profile username to generate the graph!")
        await sleep(2)
        await message.delete()
        return
    else:
        git_user = message.command[1]

    url = f"https://ghchart.rshah.org/{git_user}"
    file_name = f"{randint(1, 999)}{git_user}"

    resp = await AioHttp.get_raw(url)
    f = await aiofiles.open(f"{file_name}.svg", mode='wb')
    await f.write(resp)
    await f.close()

    try:
        drawing = svg2rlg(f"{file_name}.svg")
        renderPM.drawToFile(drawing, f"{file_name}.png")
    except UnboundLocalError:
        await message.edit("Username does not exist!")
        await sleep(2)
        await message.delete()
        return

    await asyncio.gather(
        UserBot.send_photo(
            chat_id=message.chat.id,
            photo=f"{file_name}.png",
            caption=git_user,
            reply_to_message_id=ReplyCheck(message)
        ),
        message.delete()
    )

    for file in iglob(f"{file_name}.*"):
        os.remove(file)


# Command help section
add_command_help(
    'git', [
        ['.lastcommit | .lc', 'Gets the last commit message.'],
        ['.ggraph | .commitgraph', 'Gets the commit graph for a Github user.'],
    ]
)
