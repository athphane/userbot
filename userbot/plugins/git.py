import datetime
import os

import git
import cairosvg
import aiofiles
from random import randint
from glob import iglob

from pyrogram import Filters, Message
from asyncio import sleep

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help
from userbot.helpers.aiohttp import AioHttp

@UserBot.on_message(Filters.command(['lastcommit', 'lc'], '.') & Filters.me)
async def last_commit(bot: UserBot, message: Message):
    repo = git.Repo(os.getcwd())
    master = repo.head.reference
    commit = master.commit.message.strip()
    id = master.commit.hexsha
    commit_link = f"<a href='https://github.com/athphane/userbot/commit/{id}'>{id[:7]}</a>"
    author = master.commit.author.name
    date_time = datetime.datetime.fromtimestamp(master.commit.committed_date)
    commit_msg = f"**Latest commit**: {commit_link}\n\n**Commit Message**:\n```{commit.strip()}```\n\n**By**: `{author}`\n\n**On**: `{date_time}`"
    await message.edit(commit_msg, disable_web_page_preview=True)

@UserBot.on_message(Filters.command(['ggraph', 'commitgraph'], '.') & Filters.me)
async def commit_graph(bot: UserBot, message: Message):
    if len(message.command) < 2:
        message.edit("Please provide a github profile username to generate the graph!")
        await sleep(2)
        await message.delete()
        return
    else:
        git_user = message.command[1]
    
    url = f"https://ghchart.rshah.org/{git_user}"
    resp = await AioHttp.get_raw(url)
    f = await aiofiles.open('git.svg', mode='wb')
    await f.write(resp)
    await f.close()
    
    file_name = f"{randint(1,999)}{git_user}"
    try:
        cairosvg.svg2png(url=f"{file_name}.svg", write_to=f"{file_name}.png")
    except UnboundLocalError:
        message.edit("Username does not exist!")
        await sleep(2)
        await message.delete()
        return
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=f"{file_name}.png",
        caption=git_user,
        reply_to_message_id=ReplyCheck(message)
    )
    await message.delete()
    
    for file in iglob(f"{file_name}.*"):
        os.remove(file)

# Command help section
add_command_help(
    'git', [
        ['.lastcommit | .lc', 'Gets the last commit message.'],
        ['.ggraph | .commitgraph', 'Gets the commit graph for a Github user.'],
    ]
)
