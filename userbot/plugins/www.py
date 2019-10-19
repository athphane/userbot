from datetime import datetime
import speedtest

from pyrogram import Filters, Message
from pyrogram.api import functions

from userbot import BOT

from userbot.helpers.PyroHelpers import SpeedConvert
from userbot.helpers.constants import WWW


@BOT.on_message(Filters.command("speed", ".") & Filters.me)
def speed_test(bot: BOT, message: Message):
    new_msg = message.edit(
        "`Running speed test . . .`")
    spd = speedtest.Speedtest()

    new_msg = message.edit(
        f"`{new_msg.text}`\n"
        "`Getting best server based on ping . . .`")
    spd.get_best_server()

    new_msg = message.edit(
        f"`{new_msg.text}`\n"
        "`Testing downloads speed . . .`")
    spd.download()

    new_msg = message.edit(
        f"`{new_msg.text}`\n"
        "`Testing upload speed . . .`")
    spd.upload()

    new_msg = new_msg.edit(
        f"`{new_msg.text}`\n"
        "`Getting results and preparing formatting . . .`")
    results = spd.results.dict()

    message.edit(
        WWW.SpeedTest.format(
            start=results['timestamp'],
            ping=results['ping'],
            download=SpeedConvert(results['downloads']),
            upload=SpeedConvert(results['upload']),
            isp=results['client']['isp']
        ))


@BOT.on_message(Filters.command("dc", ".") & Filters.me)
def nearest_dc(bot: BOT, message: Message):
    dc = BOT.send(
        functions.help.GetNearestDc())
    message.edit(
        WWW.NearestDC.format(
            dc.country,
            dc.nearest_dc,
            dc.this_dc))


@BOT.on_message(Filters.command("ping", ".") & Filters.me)
def ping_me(bot: BOT, message: Message):
    start = datetime.now()
    message.edit('`Pong!`')
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    message.edit(f"**Pong!**\n`{ms} ms`")
