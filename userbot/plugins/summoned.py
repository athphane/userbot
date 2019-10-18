from pyrogram import Filters, Message
from userbot import BOT
from userbot.helpers.file_sending_helpers import send_saved_image
import time
from random import randint
import datetime
import math
from userbot.database.summon import SUMMON


def human_time(*args, **kwargs):
    secs = float(datetime.timedelta(*args, **kwargs).total_seconds())
    units = [("day", 86400), ("hour", 3600), ("minute", 60), ("second", 1)]
    parts = []
    for unit, mul in units:
        if secs / mul >= 1 or mul == 1:
            if mul > 1:
                n = int(math.floor(secs / mul))
                secs -= n * mul
            else:
                n = secs if secs != int(secs) else int(secs)
            parts.append("%s %s%s" % (n, unit, "" if n == 1 else "s"))
    return ", ".join(parts)


def random_interval():
    """
    Get me a time delta between 4 hours and 12 hours.
    :return: int
    """
    rand_value = randint(14400, 43200)
    delta = (time.time() + rand_value) - time.time()
    return int(delta)


@BOT.on_message(Filters.command('summonhere', '.') & Filters.me)
def summon_here(bot: BOT, message: Message):
    chat_details = SUMMON().find_chat_id(message)

    if chat_details is not None:

        chat_id = chat_details['chat_id']

        if chat_id == message.chat.id:
            message.edit("```Summon message for this group is already enabled...```")

    elif chat_details is None:
        SUMMON().add_chat_id(message)
        message.edit("```Summon message for this group has been enabled!!```")

    time.sleep(2)
    message.delete()


@BOT.on_message(Filters.command('summonhere', '!') & Filters.me)
def not_welcome_here(bot: BOT, message: Message):
    if SUMMON().delete_chat_id(message) is True:
        message.edit("```Summon message disabled for this chat```")
    else:
        message.edit("```Summon message for this group was never enabled.```")

    time.sleep(2)
    message.delete()


@BOT.on_message(Filters.incoming & Filters.mentioned & ~Filters.reply, group=3)
def summoned(bot: BOT, message: Message):
    chat_details = SUMMON().find_chat_id(message)

    if chat_details is not None:
        if chat_details['chat_id'] == message.chat.id:
            try:
                last_send = chat_details['last_send']
                next_send = chat_details['next_send']

                if (time.time() - last_send) >= next_send:
                    send_saved_image(message, "summoned_cat", "summoned_cat.jpg")
                    last_send = time.time()
                    next_send = random_interval()
                    SUMMON().update(message, last_send, next_send)
            except:
                send_saved_image(message, "summoned_cat", "summoned_cat.jpg")
                last_send = time.time()
                next_send = random_interval()
                SUMMON().update(message, last_send, next_send)


@BOT.on_message(Filters.command('nextsummon', '.') & Filters.me, group=3)
def next_summon(bot: BOT, message: Message):
    chat_details = SUMMON().find_chat_id(message)

    if chat_details is not None:
        if chat_details['chat_id'] == message.chat.id:
            try:
                last_send = chat_details['last_send']
                next_send = chat_details['next_send']

                delta = (last_send + next_send) - time.time()

                message.edit("'''{}'''".format(human_time(seconds=int(delta))))
                time.sleep(2)
                message.delete()
            except:
                message.edit("```This group does not have a summon message interval```")
                time.sleep(2)
                message.delete()
        else:
            message.delete()
    else:
        message.delete()
