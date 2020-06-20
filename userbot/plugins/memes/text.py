import asyncio
import random
import re
from random import choice

from pyrogram import Filters, Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import GetUserMentionable
from userbot.helpers.aiohttp import AioHttp
from userbot.helpers.constants import MEMES
from userbot.helpers.utility import get_mock_text
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command('nice', '.') & Filters.me)
async def nice(_, message: Message):
    await message.edit("NICENICENICENICE")


@UserBot.on_message(Filters.command("compliment", ".") & Filters.me)
async def compliment_func(_, message: Message):
    try:
        data = await AioHttp().get_json('https://complimentr.com/api')
        compliment = data['compliment']
        await message.edit(
            compliment.capitalize()
        )
    except Exception:
        await message.delete()
        

@UserBot.on_message(Filters.command("devexcuse", ".") & Filters.me)
async def dev_excuse(_, message: Message):
    try:
        data = await AioHttp().get_json('https://dev-excuses-api.herokuapp.com/')
        devexcuse = data['text']
        await message.edit(
            devexcuse.capitalize()
        )
    except Exception:
        await message.delete()


@UserBot.on_message(Filters.command("reverse", ".") & Filters.me)
async def reverse(_, message: Message):
    await message.edit(
        text=MEMES.REVERSE,
    )


@UserBot.on_message(Filters.command("slap", ".") & Filters.me)
async def slap(_, message: Message):
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
        except Exception:
            await message.edit("`Can't slap this person, need to fetch some sticks and stones!!`")


@UserBot.on_message((Filters.command("-_-", "") | Filters.command("ok", ".")) & Filters.me)
async def ok(_, message: Message):
    okay = "-_-"
    for _ in range(10):
        okay = okay[:-1] + "_-"
        await message.edit(okay, parse_mode=None)


@UserBot.on_message((Filters.command(";_;", "") | Filters.command(['sad', 'cri'], ".")) & Filters.me)
async def sad_cri(_, message: Message):
    cri = ";_;"
    for _ in range(10):
        cri = cri[:-1] + "_;"
        await message.edit(cri, parse_mode=None)


@UserBot.on_message(Filters.regex("^\.?oof$") & Filters.me)
async def oof(_, message: Message):
    oof = "Oo "
    for _ in range(10):
        oof = oof[:-1] + "of"
        await message.edit(oof, parse_mode=None)


@UserBot.on_message(Filters.command('mockt', '.') & Filters.me)
async def mock_text(_, message: Message):
    cmd = message.command

    mock_t = ""
    if len(cmd) > 1:
        mock_t = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        mock_t = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("I need something to mock")
        await asyncio.sleep(2)
        await message.delete()
        return

    input_str = mock_t
    if not input_str:
        await message.edit("`gIvE sOMEtHInG tO MoCk!`")
        return
    reply_text = get_mock_text(input_str.lower())

    await message.edit(reply_text)


@UserBot.on_message(Filters.command("insult", ".") & Filters.me)
async def insult(_, message: Message):
    try:
        await message.edit("`Generating insult...`")
        data = await AioHttp().get_json('https://evilinsult.com/generate_insult.php?lang=en&type=json')
        req = data['insult']
        await message.edit(
            req
        )
    except Exception:
        await message.edit("`Failed to generate insult...`")
        await asyncio.sleep(2)
        await message.delete()


@UserBot.on_message(Filters.command("f", ".", case_sensitive=True) & Filters.me)
async def pay_respects(_, message: Message):
    paytext = "FF"
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
        paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
        paytext * 2, paytext * 2)

    await message.edit(pay)


@UserBot.on_message(Filters.command("F", ".", case_sensitive=True) & Filters.me)
async def pay_respects_new(_, message: Message):
    pay = (
        "██████╗\n"
        "██╔═══╝\n"
        "█████╗\n"
        "██╔══╝\n"
        "██║\n"
        "╚═╝"
    )
    await message.edit(pay)


@UserBot.on_message(Filters.command("f", "#") & Filters.me)
async def calligraphic_f(_, message: Message):
    pay = (
        "⠀⠀⠀⢀⡤⢶⣶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⢀⣠⣤⣤⣤⣿⣧⣀⣀⣀⣀⣀⣀⣀⣀⣤⡄⠀\n"
        "⢠⣾⡟⠋⠁⠀⠀⣸⠇⠈⣿⣿⡟⠉⠉⠉⠙⠻⣿⡀\n"
        "⢺⣿⡀⠀⠀⢀⡴⠋⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠙⠇\n"
        "⠈⠛⠿⠶⠚⠋⣀⣤⣤⣤⣿⣿⣇⣀⣀⣴⡆⠀⠀⠀\n"
        "⠀⠀⠀⠀⠠⡞⠋⠀⠀⠀⣿⣿⡏⠉⠛⠻⣿⡀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠈⠁⠀⠀\n"
        "⠀⠀⣠⣶⣶⣶⣶⡄⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⢰⣿⠟⠉⠙⢿⡟⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⢸⡟⠀⠀⠀⠘⠀⠀⠀⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠈⢿⡄⠀⠀⠀⠀⠀⣼⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠙⠷⠶⠶⠶⠿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀\n"
    )
    await message.edit(pay)


normiefont = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
weebyfont = ['卂', '乃', '匚', '刀', '乇', '下', '厶', '卄', '工', '丁', '长', '乚', '从', '𠘨', '口', '尸', '㔿', '尺', '丂', '丅', '凵',
             'リ', '山', '乂', '丫', '乙']


def weebify_text(raw_text):
    for normie_char in raw_text:
        if normie_char in normiefont:
            weeby_char = weebyfont[normiefont.index(normie_char)]
            raw_text = raw_text.replace(normie_char, weeby_char)
    return raw_text


@UserBot.on_message(Filters.command(['weeb', 'weebify'], ".") & Filters.me)
async def weebify(_, message: Message):
    cmd = message.command

    raw_text = ""
    if len(cmd) > 1:
        raw_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        raw_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit(f"`{weebify_text('Could not weebify...')}`")
        await asyncio.sleep(2)
        await message.delete()
        return

    await message.edit(weebify_text(raw_text))


@UserBot.on_message(Filters.command('vapor', '.') & Filters.me)
async def vapor(_, message: Message):
    cmd = message.command

    vapor_text = ""
    if len(cmd) > 1:
        vapor_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        vapor_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
        await asyncio.sleep(2)
        await message.delete()
        return

    reply_text = []

    for char in vapor_text:
        if 0x21 <= ord(char) <= 0x7F:
            reply_text.append(chr(ord(char) + 0xFEE0))
        elif ord(char) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(char)

    await message.edit("".join(reply_text))


@UserBot.on_message(Filters.command('stretch', '.') & Filters.me)
async def stretch(_, message: Message):
    cmd = message.command

    stretch_text = ""
    if len(cmd) > 1:
        stretch_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        stretch_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Giiiiiiiv sooooooomeeeeeee teeeeeeext!`")
        await asyncio.sleep(2)
        await message.delete()
        return

    count = random.randint(3, 10)
    reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count),
                        stretch_text)
    await message.edit(reply_text)


@UserBot.on_message(Filters.command('beemoviescript', '.') & Filters.me)
async def bee_movie_script(_, message: Message):
    await message.edit(f"Here is the entire Bee Movie script.\nhttps://nekobin.com/bevodokate")
                           
                           
@UserBot.on_message(Filters.command(["ht"], ".") & Filters.me)
async def heads_tails(_, message: Message):
    coin_sides = ['Heads', 'Tails']
    ht = f"Heads or Tails? `{choice(coin_sides)}`"
    await message.edit(ht)


@UserBot.on_message(Filters.command("ht", ".") & Filters.me)
async def heads_tails(_, message: Message):
    coin_sides = ['Heads', 'Tails']
    ht = f"Heads or Tails?\n`{choice(coin_sides)}`"
    await message.edit(ht)


# Command help section
add_command_help(
    'text', [
        ['.nice', 'Replaces command with NICENICENICENICE.'],
        ['.compliment', 'Replaces command with a nice compliment.'],
        ['.devexcuse', 'Replaces command with an excuse that a developer would give.'],
        ['.reverse', 'Sends ASCII version of the Uno reverse card.'],
        ['.slap', 'Sends a randomly generated slap text. Can become very random at some times.'],
        ['.insult', 'Sends a randomly generated insult. Can become very random at some times.'],
        ['.vapor', 'Vaporizes the text.'],
        ['.weeb `or` .weebify', 'Weebifies the text.'],
        ['.ok', 'Sends -_____- with a fast animation.'],
        ['-_-', 'Extends to -________-'],
        ['.f', 'Pay respects'],
        ['.F', 'Pay respects but filled'],
        ['#f', 'Pay respects but calligraphy.'],
        ['.mockt', 'Mock (text only version)'],
        ['.dice', 'Send dice animation'],
        ['.target', 'Send target animation'],
        ['oof', 'Oof'],
        [';_; `or` .sad `or` cri', ';_;'],
        ['.ht', 'Heads or Tails'],
    ]
)
