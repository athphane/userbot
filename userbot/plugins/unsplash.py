import asyncio

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.aiohttp_helper import AioHttp
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['unsplash', 'pic'], ".") & Filters.me)
async def unsplash_pictures(_, message: Message):
    cmd = message.command

    if len(cmd) > 1 and isinstance(cmd[1], str):
        keyword = cmd[1]

        if len(cmd) > 2 and int(cmd[2]) < 10:
            await message.edit('```Getting Pictures```')
            count = int(cmd[2])
            for _ in range(0, count):
                img = await AioHttp().get_url(f"https://source.unsplash.com/1600x900/?{keyword}")
                await UserBot.send_photo(message.chat.id, str(img))

            await message.delete()
            return
        else:
            await message.edit('```Getting Picture```')
            img = await AioHttp().get_url(f"https://source.unsplash.com/1600x900/?{keyword}")
            await asyncio.gather(
                message.delete(),
                UserBot.send_photo(message.chat.id, str(img))
            )


# Command help section
add_command_help(
    'unsplash', [
        ['.unsplash __or__ .pic', 'Send random pic of keyword first argument.'],
    ]
)
