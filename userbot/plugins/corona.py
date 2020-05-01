import requests
from prettytable import PrettyTable
from time import sleep
from userbot import UserBot
from pyrogram import Filters, Message
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(["c"], ".") & Filters.me)
async def corona_all(bot: UserBot, message: Message):
    try:
        r = requests.get("https://corona.lmao.ninja/v2/all").json()
        all_cases = f"<b>Global Totals</b>\nCases: {r['cases']:,}\nDeaths: {r['deaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}"
        await message.edit(all_cases)
    except:
        await message.edit("```The corona API could not be reached```")
        sleep(3)
        await message.delete()


@UserBot.on_message(Filters.command(["cs"], ".") & Filters.me)
async def corona_search(bot: UserBot, message: Message):
    cmd = message.command

    if not (len(cmd) >= 2):
        await message.edit('```Not enough params provided```')
        sleep(3)
        await message.delete()
        return

    country = cmd[1]
    await message.edit(f"```Getting Corona statistics for {country}```")

    
    r = requests.get(f"https://corona.lmao.ninja/v2/countries/{country}").json()
    if "cases" not in r:
        await message.edit("```The corona API could not be reached```")
        sleep(3)
        await message.delete()
    else:
        #country_cases = f"<b>Cases for {r['country']}</b>\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
        cs = PrettyTable()
        cs.header = False
        cs.title = f"Corona Cases in {r['country']}"
        cs.add_row(["Cases", r["cases"]])
        cs.add_row(["Cases Today", r["todayCases"]])
        cs.add_row(["Deaths", r["deaths"]])
        cs.add_row(["Deaths Today", r["todayDeaths"]])
        cs.add_row(["Recovered", r["recovered"]])
        cs.add_row(["Active", r["active"]])
        cs.add_row(["Critical", r["critical"]])
        cs.add_row(["Cases/Million", r["casesPerOneMillion"]])
        cs.add_row(["Deaths/Million", r["deathsPerOneMillion"]])
        cs.add_row(["Tests", r["tests"]])
        cs.add_row(["Tests/Million", r["testsPerOneMillion"]])
        await message.edit(cs)


add_command_help(
    'corona', [
        ['.c', 'Sends global corona stats: cases, deaths, recovered, and active cases'],
        ['.cs Country',
         'Sends cases, new cases, deaths, new deaths, recovered, active cases, critical cases, and cases/deaths per one million people for a specific country']
    ]
)
