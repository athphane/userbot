import json
import requests
from userbot import UserBot, LOG_GROUP
from pyrogram import Filters, Message, ChatMember
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command("spamhammer", ".") & Filters.me)
async def spamhammer(bot: UserBot, message: Message):
    await message.edit("```Initializing the database```")

    url = 'https://feed.spamwat.ch/'

    content = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
        }
    )

    spam_ids = []
    for x in content.iter_lines():
        line: dict = json.loads(x)
        the_id = line.get('id')
        if the_id not in spam_ids:
            spam_ids.append(the_id)

    await message.edit("Starting to kick spam accounts.")

    count = 0
    async for member in bot.iter_chat_members(message.chat.id):
        member: ChatMember = member
        if member.user.id in spam_ids:
            try:
                await bot.kick_chat_member(message.chat.id, member.user.id, until_date=0)
                await message.edit(f"```Kicked {count} spam accounts from here.```")
                count += 1
            except:
                ban_message = (
                    f"{member.user.id} could not be banned from Baivaru Requests for some reason."
                )
                await bot.send_message(LOG_GROUP, ban_message)

            ban_message = (
                f"{member.user.id} just got banned from Baivaru Requests."
            )
            await bot.send_message(LOG_GROUP, ban_message)

    print(f"```Kicked {count} spam accounts from here.```")
    # await message.edit(f"```Kicked {count} spam accounts from here.```")


add_command_help(
    'spamhammer', [['.spamhammer', 'Finds spam accounts in groups and incinerates them.']]
)
