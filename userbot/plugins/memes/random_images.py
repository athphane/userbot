import requests
import re
from userbot import UserBot
from pyrogram import Filters, Message
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help

animal = r"([^.]*)$"
ok_exts = ["jpg", "jpeg", "png"]


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


# Command help section
add_command_help(
    'images', [
        ['.cat', 'Sends a random picture of a cat. Can be used without the period at the beginning.'],
        ['.dog', 'Sends a random picture of a dog. Can be used without the period at the beginning.'],
    ]
)
