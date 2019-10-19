import requests
import re
from time import sleep
from random import choice
from collections import deque
from userbot import BOT
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


@BOT.on_message(Filters.command(["dog", "doggo"], "") & Filters.me)
def dog(bot: BOT, message: Message):
    BOT.send_photo(
        chat_id=message.chat.id,
        photo=_prep_dog(),
        caption="doggo",
        reply_to_message_id=ReplyCheck(message)
    )
    message.delete()


@BOT.on_message(Filters.command(["cat", "catto"], "") & Filters.me)
def cat(bot: BOT, message: Message):
    BOT.send_photo(
        chat_id=message.chat.id,
        photo=_prep_cat(),
        caption="catto",
        reply_to_message_id=ReplyCheck(message)
    )
    message.delete()


@BOT.on_message(Filters.command(["nice"], ".") & Filters.me)
def reverse(bot: BOT, message: Message):
    BOT.send_message(
        chat_id=message.chat.id,
        text="NICENICENICENICE",
        reply_to_message_id=ReplyCheck(message)
    )
    message.delete()


@BOT.on_message(Filters.command(["reverse"], ".") & Filters.me)
def reverse(bot: BOT, message: Message):
    BOT.send_message(
        chat_id=message.chat.id,
        text=MEMES.REVERSE,
        reply_to_message_id=ReplyCheck(message)
    )
    message.delete()


@BOT.on_message(Filters.command("mock", ".") & Filters.me)
def mock_people(bot: BOT, message: Message):
    cmd = message.command

    if len(cmd) > 1:
        mock_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        mock_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        message.edit("gIvE sOMEtHInG tO MoCk")
        sleep(2)
        message.delete()
        return

    mock_results = BOT.get_inline_bot_results(
        "stickerizerbot",
        "#7" + mock_text)

    try:
        BOT.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=mock_results.query_id,
            result_id=mock_results.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)

    message.delete()


@BOT.on_message(Filters.command("animegirl", ".") & Filters.me)
def mock_people(bot: BOT, message: Message):
    cmd = message.command

    if len(cmd) > 1:
        anime_girl_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        anime_girl_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        message.edit("`Senpai I need something to say :(`")
        sleep(2)
        message.delete()
        return

    mock_results = BOT.get_inline_bot_results(
        "stickerizerbot",
        "#32" + anime_girl_text)

    try:
        BOT.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=mock_results.query_id,
            result_id=mock_results.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)
    message.delete()


@BOT.on_message(Filters.command("ggl", ".") & Filters.me)
def google_sticker(bot: BOT, message: Message):
    cmd = message.command

    if len(cmd) > 1:
        ggl_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        ggl_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        message.edit("I need something to google")
        sleep(2)
        message.delete()
        return

    ggl_result = BOT.get_inline_bot_results(
        "stickerizerbot",
        "#12" + ggl_text)
    try:
        BOT.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=ggl_result.query_id,
            result_id=ggl_result.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)
    message.delete()


@BOT.on_message(Filters.command("slap", ".") & Filters.me)
def slap(bot: BOT, message: Message):
    if message.reply_to_message is None:
        message.delete()
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
            message.edit(caption)
        except:
            message.edit("`Can't slap this person, need to fetch some sticks and stones!!`")


@BOT.on_message(Filters.command("-_-", "") & Filters.me)
def ok(bot: BOT, message: Message):
    okay = "-_-"
    for i in range(10):
        okay = okay[:-1] + "_-"
        message.edit(okay, parse_mode=None)


@BOT.on_message(Filters.command("moon", ".") & Filters.me)
def moon(bot: BOT, message: Message):
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    try:
        for x in range(32):
            sleep(0.2)
            message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except:
        message.delete()


@BOT.on_message(Filters.command("clock", ".") & Filters.me)
def clock(bot: BOT, message: Message):
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    try:
        for x in range(32):
            sleep(0.2)
            message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except:
        message.delete()


@BOT.on_message(Filters.command("vapor", ".") & Filters.me)
def vapor(bot: BOT, message: Message):
    cmd = message.command

    if len(cmd) > 1:
        vapor_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        vapor_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        message.edit("`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
        sleep(2)
        message.delete()
        return

    reply_text = list()
    for char in vapor_text:
        if 0x21 <= ord(char) <= 0x7F:
            reply_text.append(chr(ord(char) + 0xFEE0))
        elif ord(char) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(char)

    message.edit("".join(reply_text))