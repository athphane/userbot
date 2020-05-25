import asyncio
import re
from time import sleep

import requests
from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help

animal = r"([^.]*)$"
ok_exts = ["jpg", "jpeg", "png"]
animals = ['dog', 'cat', 'panda', 'fox', 'bird', 'koala']


def _prep_dog():
    ext = ''
    dog_pic = None
    while ext not in ok_exts:
        dog_pic = requests.get('https://random.dog/woof.json').json()['url']
        ext = re.search(animal, dog_pic).group(1).lower()
    return dog_pic


def _prep_cat():
    ext = ''
    cat_pic = None
    while ext not in ok_exts:
        cat_pic = requests.get('http://aws.random.cat/meow').json()['file']
        ext = re.search(animal, cat_pic).group(1).lower()
    return cat_pic


def _prep_panda():
    ext = ''
    panda_pic = None
    while ext not in ok_exts:
        panda_pic = requests.get('https://some-random-api.ml/img/panda').json()['link']
        ext = re.search(animal, panda_pic).group(1).lower()
    return panda_pic


def _prep_redpanda():
    ext = ''
    redpanda_pic = None
    while ext not in ok_exts:
        redpanda_pic = requests.get('https://some-random-api.ml/img/red_panda').json()['link']
        ext = re.search(animal, redpanda_pic).group(1).lower()
    return redpanda_pic


def _prep_bird():
    ext = ''
    bird_pic = None
    while ext not in ok_exts:
        bird_pic = requests.get('https://some-random-api.ml/img/birb').json()['link']
        ext = re.search(animal, bird_pic).group(1).lower()
    return bird_pic


def _prep_fox():
    ext = ''
    fox_pic = None
    while ext not in ok_exts:
        fox_pic = requests.get('https://some-random-api.ml/img/fox').json()['link']
        ext = re.search(animal, fox_pic).group(1).lower()
    return fox_pic


def _prep_koala():
    ext = ''
    koala_pic = None
    while ext not in ok_exts:
        koala_pic = requests.get('https://some-random-api.ml/img/koala').json()['link']
        ext = re.search(animal, koala_pic).group(1).lower()
    return koala_pic


@UserBot.on_message(Filters.regex("^\.?dog$") & Filters.me)
async def dog(bot: UserBot, message: Message):
    if message.from_user.is_self:
        await message.delete()

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=_prep_dog(),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.regex("^\.?cat$") & Filters.me)
async def cat(bot: UserBot, message: Message):
    if message.from_user.is_self:
        await message.delete()

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=_prep_cat(),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.regex("^\.?panda$") & Filters.me)
async def panda(bot: UserBot, message: Message):
    if message.from_user.is_self:
        await message.delete()

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=_prep_panda(),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.regex("^\.?redpanda$") & Filters.me)
async def redpanda(bot: UserBot, message: Message):
    if message.from_user.is_self:
        await message.delete()

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=_prep_redpanda(),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.regex("^\.?bird$") & Filters.me)
async def bird(bot: UserBot, message: Message):
    if message.from_user.is_self:
        await message.delete()

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=_prep_bird(),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.regex("^\.?fox$") & Filters.me)
async def fox(bot: UserBot, message: Message):
    if message.from_user.is_self:
        await message.delete()

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=_prep_fox(),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.regex("^\.?koala$") & Filters.me)
async def koala(bot: UserBot, message: Message):
    if message.from_user.is_self:
        await message.delete()

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=_prep_koala(),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.command('fact', '.'))
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
            fact_text = requests.get(fact_link).json()['fact']
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

# Command help section
add_command_help(
    'animals', [
        ['.cat', 'Sends a random picture of a cat. Can be used without the period at the beginning.'],
        ['.dog', 'Sends a random picture of a dog. Can be used without the period at the beginning.'],
        ['.panda', 'Sends a random picture of a panda. Can be used without the period at the beginning.'],
        ['.redpanda', 'Sends a random picture of a redpanda. Can be used without the period at the beginning.'],
        ['.bird', 'Sends a random picture of a bird. Can be used without the period at the beginning.'],
        ['.fox', 'Sends a random picture of a fox. Can be used without the period at the beginning.'],
        ['.koala', 'Sends a random picture of a koala. Can be used without the period at the beginning.'],
        ['These commands', "Works without the command prefix also"]
    ]
)


fact_help = []
for x in animals:
    fact_help.append([f".fact {x}", f"Send a random fact about {x}"])

add_command_help(
    'facts', fact_help
)