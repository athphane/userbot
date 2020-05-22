import asyncio
from time import sleep
import requests
from random import choice
from userbot import UserBot
from pyrogram import Filters, Message
from userbot.helpers.constants import MEMES
from userbot.helpers.PyroHelpers import ReplyCheck, GetUserMentionable
from userbot.plugins.help import add_command_help

animals = ['dog', 'cat', 'panda', 'fox', 'bird', 'koala']


@UserBot.on_message(Filters.command(["nice"], ".") & Filters.me)
async def nice(bot: UserBot, message: Message):
    await message.delete()
    await bot.send_message(
        chat_id=message.chat.id,
        text="NICENICENICENICE",
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.command(["compliment"], ".") & Filters.me)
async def compliment_func(bot: UserBot, message: Message):
    try:
        compliment = requests.get('https://complimentr.com/api').json()['compliment']
        await message.edit(
            compliment.capitalize()
        )
    except:
        await message.delete()


@UserBot.on_message(Filters.command(["devexcuse"], ".") & Filters.me)
async def dev_excuse(bot: UserBot, message: Message):
    try:
        devexcuse = requests.get('https://dev-excuses-api.herokuapp.com/').json()['text']
        await message.edit(
            devexcuse.capitalize()
        )
    except:
        await message.delete()


@UserBot.on_message(Filters.command(["reverse"], ".") & Filters.me)
async def reverse(bot: UserBot, message: Message):
    await message.delete()
    await bot.send_message(
        chat_id=message.chat.id,
        text=MEMES.REVERSE,
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.command("slap", ".") & Filters.me)
async def slap(bot: UserBot, message: Message):
    if message.reply_to_message is None:
        await message.delete()
    else:
        replied_user = message.reply_to_message.from_user

        if message.from_user.id is replied_user.id:
            return

        slapped = GetUserMentionable(replied_user)

        temp = choice(MEMES.SLAP_TEMPLATES)
        item = choice(MEMES.ITEMS)
        hit = choice(MEMES.HIT)
        throw = choice(MEMES.THROW)
        where = choice(MEMES.WHERE)

        caption = temp.format(victim=slapped, item=item, hits=hit, throws=throw, where=where)

        try:
            await message.edit(caption)
        except:
            await message.edit("`Can't slap this person, need to fetch some sticks and stones!!`")


@UserBot.on_message(Filters.command("-_-", "") | Filters.command("ok", ".") & Filters.me)
async def ok(bot: UserBot, message: Message):
    okay = "-_-"
    for i in range(10):
        okay = okay[:-1] + "_-"
        await message.edit(okay, parse_mode=None)


@UserBot.on_message(Filters.command('fact', '.'))
async def fact(bot: UserBot, message: Message):
    cmd = message.command

    if not (len(cmd) >= 2):
        await message.edit('```Not enough params provided```')
        sleep(3)
        await message.delete()
        return

    await message.edit(f"```Getting {cmd[1]} fact```")
    link = "https://some-random-api.ml/facts/{animal}"

    if cmd[1].lower() in animals:
        fact_link = link.format(animal=cmd[1].lower())
        try:
            fact_text = requests.get(fact_link).json()['fact']
        except:
            await message.edit("```The fact API could not be reached```")
            sleep(3)
            await message.delete()
        else:
            await message.edit(fact_text, disable_web_page_preview=True)


@UserBot.on_message(Filters.command(["insult"], ".") & Filters.me)
async def insult(bot: UserBot, message: Message):
    try:
        req = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json").json()['insult']
        await message.edit(
            req
        )
    except:
        await message.delete()


@UserBot.on_message(Filters.command(["f"], ".", case_sensitive=True) & Filters.me)
async def pay_respects(bot: UserBot, message: Message):
    paytext = "FF"
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
        paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
        paytext * 2, paytext * 2)

    await message.edit(pay)


@UserBot.on_message(Filters.command(["F"], ".", case_sensitive=True) & Filters.me)
async def pay_respects_new(bot: UserBot, message: Message):
    pay = (
        "██████╗\n"
        "██╔═══╝\n"
        "█████╗\n"
        "██╔══╝\n"
        "██║\n"
        "╚═╝"
    )
    await message.edit(pay)


@UserBot.on_message(Filters.command(["g"], ".") & Filters.me)
async def gerey(bot: UserBot, message: Message):
    gerey = "ގެރޭ"
    await message.edit(gerey)


# Command help section
add_command_help(
    'text', [
        ['.nice', 'Replaces command with NICENICENICENICE.'],
        ['.compliment', 'Replaces command with a nice compliment.'],
        ['.devexcuse', 'Replaces command with an excuse that a developer would give.'],
        ['.reverse', 'Sends ASCII version of the Uno reverse card.'],
        ['.slap', 'Sends a randomly generated slap text. Can become very random at some times.'],
        ['.insult', 'Sends a randomly generated insult. Can become very random at some times.'],
        ['.ok', 'Sends -_____- with a fast animation.'],
        ['-_-', 'Extends to -________-'],
        ['.f', 'Pay respects'],
        ['.F', 'Pay respects but filled'],
        ['.g', 'Gerey'],
    ]
)

fact_help = []
for x in animals:
    fact_help.append([f".fact {x}", f"Send a random fact about {x}"])

add_command_help(
    'facts', fact_help
)
