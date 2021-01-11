import asyncio
from collections import deque
from random import randint

from pyrogram import filters
from pyrogram.types import Message
from userbot import UserBot
from userbot.plugins.help import add_command_help

emojis = {
    "moon": list("🌗🌘🌑🌒🌓🌔🌕🌖"),
    "clock": list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"),
    "thunder": list("☀️🌤️⛅🌥️☁️🌩️🌧️⛈️⚡🌩️🌧️🌦️🌥️⛅🌤️☀️"),
    "earth": list("🌏🌍🌎🌎🌍🌏🌍🌎"),
    "heart": list("❤️🧡💛💚💙💜🖤"),
}
emoji_commands = [x for x in emojis]


@UserBot.on_message(filters.command(emoji_commands, ".") & filters.me)
async def emoji_cycle(_, message: Message):
    deq = deque(emojis[message.command[0]])
    try:
        for _ in range(randint(16, 32)):
            await asyncio.sleep(0.3)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except Exception:
        await message.delete()


special_emojis_dict = {
    "target": {"emoji": "🎯", "help": "The special target emoji"},
    "dice": {"emoji": "🎲", "help": "The special dice emoji"},
    "bb": {"emoji": "🏀", "help": "The special basketball emoji"},
    "soccer": {"emoji": "⚽️", "help": "The special football emoji"},
}
special_emoji_commands = [x for x in special_emojis_dict]


@UserBot.on_message(filters.command(special_emoji_commands, ".") & filters.me)
async def special_emojis(_, message: Message):
    emoji = special_emojis_dict[message.command[0]]
    await message.delete()
    await UserBot.send_dice(message.chat.id, emoji["emoji"])


# Command help section
special_emoji_help = [
    [".moon", "Cycles all the phases of the moon emojis."],
    [".clock", "Cycles all the phases of the clock emojis."],
    [".thunder", "Cycles thunder."],
    [".heart", "Cycles heart emojis."],
    [".earth `or` .globe", "Make the world go round."],
]

for x in special_emojis_dict:
    command = f".{x}"
    special_emoji_help.append([command, special_emojis_dict[x]["help"]])

add_command_help("emoji", special_emoji_help)
