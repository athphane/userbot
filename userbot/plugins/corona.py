import asyncio
import datetime

from prettytable import PrettyTable
from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.helpers.aiohttp_helper import AioHttp
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command("c", ".") & filters.me)
async def corona_all(_, message: Message):
    try:
        r = await AioHttp().get_json("https://corona.lmao.ninja/v2/all?yesterday=true")
        last_updated = datetime.datetime.fromtimestamp(r["updated"] / 1000).strftime(
            "%Y-%m-%d %I:%M:%S"
        )

        ac = PrettyTable()
        ac.header = False
        ac.title = "Global Statistics"
        ac.add_row(["Cases", f"{r['cases']:,}"])
        ac.add_row(["Cases Today", f"{r['todayCases']:,}"])
        ac.add_row(["Deaths", f"{r['deaths']:,}"])
        ac.add_row(["Deaths Today", f"{r['todayDeaths']:,}"])
        ac.add_row(["Recovered", f"{r['recovered']:,}"])
        ac.add_row(["Active", f"{r['active']:,}"])
        ac.add_row(["Critical", f"{r['critical']:,}"])
        ac.add_row(["Cases/Million", f"{r['casesPerOneMillion']:,}"])
        ac.add_row(["Deaths/Million", f"{r['deathsPerOneMillion']:,}"])
        ac.add_row(["Tests", f"{r['tests']:,}"])
        ac.add_row(["Tests/Million", f"{r['testsPerOneMillion']:,}"])
        ac.align = "l"

        await message.edit(f"```{str(ac)}```\nLast updated on: {last_updated}")
    except Exception as e:
        await message.edit("`The corona API could not be reached`")
        print(e)
        await asyncio.sleep(3)
        await message.delete()


@UserBot.on_message(filters.command("cs", ".") & filters.me)
async def corona_search(_, message: Message):
    cmd = message.command

    if not (len(cmd) >= 2):
        await message.edit("```Not enough params provided```")
        await asyncio.sleep(3)
        await message.delete()
        return

    country = cmd[1]
    await message.edit(f"```Getting Corona statistics for {country}```")

    r = await AioHttp().get_json(f"https://corona.lmao.ninja/v2/countries/{country}")
    if "cases" not in r:
        await message.edit("```The country could not be found!```")
        await asyncio.sleep(3)
        await message.delete()
    else:
        last_updated = datetime.datetime.fromtimestamp(r["updated"] / 1000).strftime(
            "%Y-%m-%d %I:%M:%S"
        )

        cc = PrettyTable()
        cc.header = False
        country = r["countryInfo"]["iso3"] if len(r["country"]) > 12 else r["country"]
        cc.title = f"Corona Cases in {country}"
        cc.add_row(["Cases", f"{r['cases']:,}"])
        cc.add_row(["Cases Today", f"{r['todayCases']:,}"])
        cc.add_row(["Deaths", f"{r['deaths']:,}"])
        cc.add_row(["Deaths Today", f"{r['todayDeaths']:,}"])
        cc.add_row(["Recovered", f"{r['recovered']:,}"])
        cc.add_row(["Active", f"{r['active']:,}"])
        cc.add_row(["Critical", f"{r['critical']:,}"])
        cc.add_row(["Cases/Million", f"{r['casesPerOneMillion']:,}"])
        cc.add_row(["Deaths/Million", f"{r['deathsPerOneMillion']:,}"])
        cc.add_row(["Tests", f"{r['tests']:,}"])
        cc.add_row(["Tests/Million", f"{r['testsPerOneMillion']:,}"])
        cc.align = "l"
        await message.edit(f"```{str(cc)}```\nLast updated on: {last_updated}")


add_command_help(
    "corona",
    [
        [".c", "Sends global corona stats: cases, deaths, recovered, and active cases"],
        [
            ".cs Country",
            "Sends cases, new cases, deaths, new deaths, recovered, active cases, critical cases, "
            "and cases/deaths per one million people for a specific country",
        ],
    ],
)
