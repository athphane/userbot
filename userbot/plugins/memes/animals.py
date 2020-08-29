import asyncio
import re
from time import sleep

from pyrogram import filters
from pyrogram.types import Message
from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.helpers.aiohttp_helper import AioHttp
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
        data = await AioHttp().get_json(animal_data['url'])
        image = data[animal_data['key']]
        ext = re.search(animal, image).group(1).lower()
    return image


@UserBot.on_message(filters.command(animals, ['.', '']) & filters.me)
async def animal_image(_, message: Message):
    if len(message.command) > 1:
        return

    animal_data = animals_data[message.command[0]]
    await message.delete()
    await UserBot.send_photo(
        chat_id=message.chat.id,
        photo=await prep_animal_image(animal_data),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(filters.command('fact', '.') & filters.me)
async def fact(_, message: Message):
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
            data = await AioHttp().get_json(fact_link)
            fact_text = data['fact']
        except Exception:
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

add_command_help(
    'facts', [[f".fact {x}", f"Send a random fact about {x}"] for x in animals if x != 'redpanda']
)
