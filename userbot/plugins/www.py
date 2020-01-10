from datetime import datetime
import speedtest
from pyrogram import Filters, Message
from pyrogram.api import functions
from userbot import UserBot
from userbot.helpers.PyroHelpers import SpeedConvert
from userbot.helpers.constants import WWW
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(["speed", 'speedtest'], ".") & Filters.me)
async def speed_test(bot: UserBot, message: Message):
    new_msg = await message.edit(
        "`Running speed test . . .`")
    spd = speedtest.Speedtest()

    new_msg = await message.edit(
        f"`{new_msg.text}`\n"
        "`Getting best server based on ping . . .`")
    spd.get_best_server()

    new_msg = await message.edit(
        f"`{new_msg.text}`\n"
        "`Testing download speed . . .`")
    spd.download()

    new_msg = await message.edit(
        f"`{new_msg.text}`\n"
        "`Testing upload speed . . .`")
    spd.upload()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n"
        "`Getting results and preparing formatting . . .`")
    results = spd.results.dict()

    await message.edit(
        WWW.SpeedTest.format(
            start=results['timestamp'],
            ping=results['ping'],
            download=SpeedConvert(results['download']),
            upload=SpeedConvert(results['upload']),
            isp=results['client']['isp']
        ))


@UserBot.on_message(Filters.command("dc", ".") & Filters.me)
async def nearest_dc(bot: UserBot, message: Message):
    dc = await bot.send(
        functions.help.GetNearestDc())
    await message.edit(
        WWW.NearestDC.format(
            dc.country,
            dc.nearest_dc,
            dc.this_dc))


@UserBot.on_message(Filters.command("ping", ".") & Filters.me)
async def ping_me(bot: UserBot, message: Message):
    start = datetime.now()
    await message.edit('`Pong!`')
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await message.edit(f"**Pong!**\n`{ms} ms`")


add_command_help(
    'www', [
        ['.ping', 'Calculates ping time between you and Telegram.'],
        ['.dc', 'Get\'s your Telegram DC.'],
        ['.speedtest', 'Runs a speedtest on the server this userbot is hosted.. Flex on them haters. With an in '
                       'Telegram Speedtest of your server..'],
    ]
)