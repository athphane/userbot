import asyncio
from collections import deque
from time import sleep

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

emojis = {
    'moon': list("🌗🌘🌑🌒🌓🌔🌕🌖"),
    'clock': list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"),
    'thunder': list("☀️🌤️⛅🌥️☁️🌩️🌧️⛈️⚡🌩️🌧️🌦️🌥️⛅🌤️☀️"),
    'earth': list("🌏🌍🌎🌎🌍🌏🌍🌎"),
    'heart': list("❤️🧡💛💚💙💜🖤"),
}
emoji_commands = [x for x in emojis]


@UserBot.on_message(Filters.command(emoji_commands, ".") & Filters.me)
async def emoji_cycle(bot: UserBot, message: Message):
    deq = deque(emojis[message.command[0]])
    try:
        for x in range(32):
            await asyncio.sleep(0.3)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except:
        await message.delete()


add_command_help(
    'emoji', [
        ['.moon', 'Cycles all the phases of the moon emojis.'],
        ['.clock', 'Cycles all the phases of the clock emojis.'],
        ['.thunder', 'Cycles thunder.'],
        ['.heart', 'Cycles heart emojis.'],
        ['.earth `or` .globe', 'Make the world go round.'],
    ]
)
