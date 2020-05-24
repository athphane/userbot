import asyncio
import os
import time

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['skyrim', 'skill'], ".") & Filters.me)
async def skyrim(bot: UserBot, message: Message):
    if len(message.command) >= 2:
        text = message.command[1]
    else:
        await message.edit("```Not enough params```")
        await asyncio.sleep(3)
        await message.delete()
        return

    level = message.command[2] if len(message.command) >= 3 else 100

    try:
        try:
            if os.name == 'nt':
                os.system(f"venv\\Scripts\\activate && python userbot\\helpers\\skyrim.py \"{text}\" {level}")
            else:
                os.system(f". venv/bin/activate && python userbot//helpers//skyrim.py \"{text}\" {level}")
        except:
            await message.edit("```Failed to generate skill```")
            time.sleep(2)
            await message.delete()

        try:
            await bot.send_photo(
                message.chat.id,
                'userbot/downloads/skyrim.png',
                reply_to_message_id=ReplyCheck(message)
            )
            await message.delete()
        except:
            await message.edit("```Failed to send skill```")
            time.sleep(2)
            await message.delete()
        finally:
            os.remove('userbot/downloads/skyrim.png')
    except Exception as e:
        print(e)

# Command help section
add_command_help(
    'skyrim', [
        ['.skyrim', 'Generate skyrim skill image.\n .skyrim <before> <after>'],
        ['.skill', 'Generate skyrim skill image.\n .skill <before> <after>'],
    ]
)
