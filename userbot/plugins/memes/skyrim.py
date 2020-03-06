from userbot import UserBot
from pyrogram import Filters, Message
from userbot.helpers.PyroHelpers import ReplyCheck
import os
import time


@UserBot.on_message(Filters.command(["skyrim"], ".") & Filters.me)
async def skyrim(bot: UserBot, message: Message):
    if len(message.command) >= 2:
        text = message.command[1]
    else:
        await message.edit("```Not enough params```")
        return

    level = message.command[2] if len(message.command) >= 3 else 100

    try:
        try:
            if os.name == 'nt':
                os.system(f"venv\\Scripts\\activate && python userbot\\helpers\\skyrim.py {text} {level}")
            else:
                os.system(f"/bin/bash . venv/bin/activate && python userbot//helpers//skyrim.py {text} {level}")
        except:
            await message.edit("```Failed to generate skill```")
            time.sleep(2)

        try:
            await message.reply_photo('userbot/downloads/skyrim.png', reply_to_message_id=ReplyCheck(message))
            await message.delete()
        except:
            await message.edit("```Failed to send skill```")
            time.sleep(2)
        finally:
            os.remove('userbot/downloads/skyrim.png')
    except Exception as e:
        print(e)
