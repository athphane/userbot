from random import randint
import aiohttp
import shutil

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help

async def get_person():
    rand_int = str(randint(0,9999))
    url = "https://thispersondoesnotexist.com/image?randomtag=" + rand_int
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = (await resp.content.read()).decode('utf-8')
            file_name = f"{rand_int}person.jpeg"
            with open(file_name, 'wb') as file:
                shutil.copyfileobj(content, file)
    return file_name

@UserBot.on_message(Filters.command('person', '.') & Filters.me)
async def send_person(bot: UserBot, message: Message):
    try:
        photo = await get_person()
    except Exception as err:
        print(err)
        await message.edit("Error occured while fetching random person")
        return
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption="persono",
        reply_to_message_id=ReplyCheck(message)
    )
    await message.delete()
