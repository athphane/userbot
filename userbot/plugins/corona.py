import requests
from time import sleep
from userbot import UserBot
from pyrogram import Filters, Message
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(["c"], ".") & Filters.me)
async def corona_all(bot: UserBot, message: Message):
    try:
        r = requests.get("https://corona.lmao.ninja/all").json()
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

    try:
        r = requests.get(f"https://corona.lmao.ninja/countries/{country}").json()
    except:
        await message.edit("```The corona API could not be reached```")
        sleep(3)
        await message.delete()
    else:
        country_cases = f"<b>Cases for {r['country']}</b>\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
        await message.edit(country_cases)


add_command_help(
    'corona', [
        ['.c', 'Sends global corona stats: cases, deaths, recovered, and active cases'],
        ['.cs Country',
         'Sends cases, new cases, deaths, new deaths, recovered, active cases, critical cases, and cases/deaths per one million people for a specific country']
    ]
)
