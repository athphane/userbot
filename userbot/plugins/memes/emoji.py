from collections import deque
from time import sleep

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command("moon", ".") & Filters.me)
async def moon(bot: UserBot, message: Message):
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    try:
        for x in range(32):
            sleep(0.2)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except:
        await message.delete()


@UserBot.on_message(Filters.command("clock", ".") & Filters.me)
async def clock(bot: UserBot, message: Message):
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    try:
        for x in range(32):
            sleep(0.2)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except:
        await message.delete()


@UserBot.on_message(Filters.command("thunder", ".") & Filters.me)
async def thunder(bot: UserBot, message: Message):
    deq = deque(list("☀️🌤️⛅🌥️☁️🌩️🌧️⛈️⚡🌩️🌧️🌦️🌥️⛅🌤️☀️"))
    try:
        for x in range(32):
            sleep(0.2)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except:
        await message.delete()


@UserBot.on_message(Filters.command(['earth', 'globe'], ".") & Filters.me)
async def globe(bot: UserBot, message: Message):
    deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
    try:
        for x in range(32):
            sleep(0.2)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except:
        await message.delete()

add_command_help(
    'emoji', [
        ['.moon', 'Cycles all the phases of the moon emojis.'],
        ['.clock', 'Cycles all the phases of the clock emojis.'],
        ['.thunder', 'Cycles thunder.'],
        ['.earth `or` .globe', 'Make the world go round.'],
    ]
)
