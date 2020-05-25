import asyncio
import re
from time import sleep

import aiohttp
import requests
from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help

animal = r"([^.]*)$"
ok_exts = ["jpg", "jpeg", "png"]

animals_data = {
    'dog': {'url': 'https://random.dog/woof.json', 'key': 'url'},
    'cat': {'url': 'http://aws.random.cat/meow', 'key': 'file'},
    'panda': {'url': 'https://some-random-api.ml/img/panda', 'key': 'link'},
    'redpanda': {'url': 'https://some-random-api.ml/img/red_panda', 'key': 'link'},
    'bird': {'url': 'https://some-random-api.ml/img/birb', 'key': 'link'},
    'fox': {'url': 'https://some-random-api.ml/img/fox', 'key': 'link'},
    'koala': {'url': 'https://some-random-api.ml/img/koala', 'key': 'link'},
}

animals = [x for x in animals_data]


async def prep_animal_image(animal_data):
    ext = ''
    image = None
    while ext not in ok_exts:
        async with aiohttp.ClientSession() as session:
            async with session.get(animal_data['url']) as resp:
                data = await resp.json()

        image = data[animal_data['key']]
        ext = re.search(animal, image).group(1).lower()
    return image


@UserBot.on_message((Filters.command(animals, '.') | Filters.command(animals, '')) & Filters.me)
async def animal_image(bot: UserBot, message: Message):
    animal_data = animals_data[message.command[0]]
    await message.delete()
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=await prep_animal_image(animal_data),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.command('fact', '.') & Filters.me)
async def fact(bot: UserBot, message: Message):
    cmd = message.command

    if not (len(cmd) >= 2):
        await message.edit('```Not enough params provided```')
        await asyncio.sleep(3)
        await message.delete()
        return

    await message.edit(f"```Getting {cmd[1]} fact```")
    link = "https://some-random-api.ml/facts/{animal}"

    if cmd[1].lower() in animals:
        fact_link = link.format(animal=cmd[1].lower())
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(fact_link) as resp:
                    data = await resp.json()

            fact_text = data['fact']
        except:
            await message.edit("```The fact API could not be reached```")
            sleep(3)
            await message.delete()
        else:
            await message.edit(fact_text, disable_web_page_preview=True)
    else:
        await message.edit("`Unsupported animal...`")
        await asyncio.sleep(2)
        await message.delete()


# Animal image help
animal_image_help = []
for x in animals:
    animal_image_help.append([f".{x}", f"Sends a random picture of a {x}"])

animal_image_help.append(['These commands', "Works without the command prefix also"])

add_command_help(
    'animals', animal_image_help
)

# Animal fact help
fact_help = []
for x in animals:
    if x != 'redpanda':
        fact_help.append([f".fact {x}", f"Send a random fact about {x}"])

add_command_help(
    'facts', fact_help
)
