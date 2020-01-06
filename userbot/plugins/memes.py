import requests
import re
from time import sleep
from random import choice
from collections import deque
from userbot import UserBot
from pyrogram import Filters, Message
from userbot.helpers.constants import MEMES
from userbot.helpers.PyroHelpers import ReplyCheck, GetUserMentionable

animal = r"([^.]*)$"
ok_exts = ["jpg", "jpeg", "png"]


def _prep_dog():
    ext = ''
    while ext not in ok_exts:
        dog_pic = requests.get('https://random.dog/woof.json').json()['url']
        ext = re.search(animal, dog_pic).group(1).lower()
    return dog_pic


def _prep_cat():
    ext = ''
    while ext not in ok_exts:
        cat_pic = requests.get('http://aws.random.cat/meow').json()['file']
        ext = re.search(animal, cat_pic).group(1).lower()
    return cat_pic


@UserBot.on_message(Filters.command(["dog", "doggo"], "") & Filters.me)
async def dog(bot: UserBot, message: Message):
    await message.delete()
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=_prep_dog(),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.command(["cat", "catto"], ["", '.']) & Filters.me)
async def cat(bot: UserBot, message: Message):
    print(message)
    await message.delete()
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=_prep_cat(),
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.command(["nice"], ".") & Filters.me)
async def nice(bot: UserBot, message: Message):
    await message.delete()
    await bot.send_message(
        chat_id=message.chat.id,
        text="NICENICENICENICE",
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.command(["reverse"], ".") & Filters.me)
async def reverse(bot: UserBot, message: Message):
    await message.delete()
    await bot.send_message(
        chat_id=message.chat.id,
        text=MEMES.REVERSE,
        reply_to_message_id=ReplyCheck(message)
    )


@UserBot.on_message(Filters.command("mock", ".") & Filters.me)
async def mock_people(bot: UserBot, message: Message):
    cmd = message.command

    if len(cmd) > 1:
        mock_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        mock_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        await message.edit("gIvE sOMEtHInG tO MoCk")
        sleep(2)
        await message.delete()
        return

    mock_results = await bot.get_inline_bot_results(
        "stickerizerbot",
        "#7" + mock_text)

    try:
        await bot.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=mock_results.query_id,
            result_id=mock_results.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        await message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)

    await message.delete()


@UserBot.on_message(Filters.command("animegirl", ".") & Filters.me)
async def anime_girl(bot: UserBot, message: Message):
    cmd = message.command

    anime_girl_text = ''
    if len(cmd) > 1:
        anime_girl_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        anime_girl_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        await message.edit("`Senpai I need something to say :(`")
        sleep(2)
        await message.delete()
        return

    anime_girl_results = await bot.get_inline_bot_results(
        "stickerizerbot",
        "#32" + anime_girl_text)

    try:
        await bot.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=anime_girl_results.query_id,
            result_id=anime_girl_results.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        await message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)
    await message.delete()


@UserBot.on_message(Filters.command("ggl", ".") & Filters.me)
async def google_sticker(bot: UserBot, message: Message):
    await message.delete()
    cmd = message.command

    if len(cmd) > 1:
        ggl_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        ggl_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("I need something to google")
        sleep(2)
        await message.delete()
        return

    ggl_result = await bot.get_inline_bot_results(
        "stickerizerbot",
        "#12" + ggl_text)
    try:
        await bot.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=ggl_result.query_id,
            result_id=ggl_result.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        await message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)
        await message.delete()


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


@UserBot.on_message(Filters.command("moon", ".") & Filters.me)
async def moon(bot: UserBot, message: Message):
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    try:
        for x in range(32):
            sleep(0.2)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except:
        await message.delete()


@UserBot.on_message(Filters.command("clock", ".") & Filters.me)
async def clock(bot: UserBot, message: Message):
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    try:
        for x in range(32):
            sleep(0.2)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except:
        await message.delete()


@UserBot.on_message(Filters.command("vapor", ".") & Filters.me)
async def vapor(bot: UserBot, message: Message):
    cmd = message.command

    if len(cmd) > 1:
        vapor_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        vapor_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
        sleep(2)
        await message.delete()
        return

    reply_text = list()
    for char in vapor_text:
        if 0x21 <= ord(char) <= 0x7F:
            reply_text.append(chr(ord(char) + 0xFEE0))
        elif ord(char) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(char)

    await message.edit("".join(reply_text))


@UserBot.on_message(Filters.command("flip", prefixes=".") & Filters.me)
async def flip(bot: UserBot, message: Message):
    cmd = message.command
    mock_text = ""
    if len(cmd) > 1:
        mock_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        mock_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        await message.edit("```Give me something to flip```")
        sleep(2)
        await message.delete()
        return

    final_str = ""
    for char in mock_text:
        if char in MEMES.REPLACEMENT_MAP.keys():
            new_char = MEMES.REPLACEMENT_MAP[char]
        else:
            new_char = char
        final_str += new_char
    if mock_text != final_str:
        await message.edit(final_str)
    else:
        await message.edit(mock_text)


@UserBot.on_message(Filters.command("insult", '.'))
async def insult(bot: UserBot, message: Message):
    await message.edit(requests.get("https://insult.mattbas.org/api/insult").content.decode('utf-8'))


@UserBot.on_message(Filters.command("joke", '.'))
async def joke(bot: UserBot, message: Message):
    the_joke = requests.get("https://icanhazdadjoke.com", headers={
        'Accept': 'text/plain',
    }).content.decode('utf-8')
    await message.edit(the_joke)


@UserBot.on_message(~Filters.edited & Filters.command(["whatislove", 'wis'], '.') | Filters.command('what is love', ''))
async def joke(bot: UserBot, message: Message):
    reply = ("Baby don't hurt me\n"
             "Don't hurt me\n"
             "No more")

    if message.from_user.is_self:
        await message.edit(f"```{message.text}\n```{reply}```")
    else:
        await message.reply(f"```{reply}```")
