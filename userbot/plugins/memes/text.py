import asyncio
import random
import re
from random import choice

from pyrogram import filters
from pyrogram.types import Message
from userbot import UserBot
from userbot.helpers.PyroHelpers import GetUserMentionable
from userbot.helpers.constants import MEMES, Fs, Weebify
from userbot.helpers.utility import get_mock_text
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command("nice", ".") & filters.me)
async def nice(_, message: Message):
    await message.edit("NICENICENICENICE")


@UserBot.on_message(filters.command("reverse", ".") & filters.me)
async def reverse(_, message: Message):
    await message.edit(
        text=MEMES.REVERSE,
    )


@UserBot.on_message(filters.command("slap", ".") & filters.me)
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

        caption = temp.format(
            victim=slapped, item=item, hits=hit, throws=throw, where=where
        )

        try:
            await message.edit(caption)
        except Exception:
            await message.edit(
                "`Can't slap this person, need to fetch some sticks and stones!!`"
            )


@UserBot.on_message(
    (filters.command("-_-", "") | filters.command("ok", ".")) & filters.me
)
async def ok(_, message: Message):
    okay = "-_-"
    for _ in range(10):
        okay = okay[:-1] + "_-"
        await message.edit(okay, parse_mode=None)


@UserBot.on_message(
    (filters.command(";_;", "") | filters.command(["sad", "cri"], ".")) & filters.me
)
async def sad_cri(_, message: Message):
    cri = ";_;"
    for _ in range(10):
        cri = cri[:-1] + "_;"
        await message.edit(cri, parse_mode=None)


@UserBot.on_message(filters.regex(r"^\.?oof$") & filters.me)
async def send_oof(_, message: Message):
    oof = "Oo "
    for _ in range(10):
        oof = oof[:-1] + "of"
        await message.edit(oof, parse_mode=None)


@UserBot.on_message(filters.command("mockt", ".") & filters.me)
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


@UserBot.on_message(filters.command("brain", ".") & filters.me)
async def brain(_, message: Message):
    for x in MEMES.BRAIN:
        await asyncio.sleep(0.35)
        await message.edit(x)


@UserBot.on_message(filters.command("f", ".", case_sensitive=True) & filters.me)
async def pay_respects(_, message: Message):
    await message.edit(Fs().F)


@UserBot.on_message(filters.command("F", ".", case_sensitive=True) & filters.me)
async def pay_respects_new(_, message: Message):
    await message.edit(Fs.BIG_F)


@UserBot.on_message(filters.command("f", "#") & filters.me)
async def calligraphic_f(_, message: Message):
    await message.edit(Fs.FANCY_F)


def weebify_text(raw_text):
    for normie_char in raw_text:
        if normie_char in Weebify.NORMIE_FONT:
            weeby_char = Weebify.WEEBY_FONT[Weebify.NORMIE_FONT.index(normie_char)]
            raw_text = raw_text.replace(normie_char, weeby_char)
    return raw_text


@UserBot.on_message(filters.command(["weeb", "weebify"], ".") & filters.me)
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


@UserBot.on_message(filters.command("vapor", ".") & filters.me)
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


@UserBot.on_message(filters.command("stretch", ".") & filters.me)
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
    reply_text = re.sub(
        r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count), stretch_text
    )
    await message.edit(reply_text)


@UserBot.on_message(filters.command("beemoviescript", ".") & filters.me)
async def bee_movie_script(_, message: Message):
    await message.edit(
        "Here is the entire Bee Movie script.\nhttps://nekobin.com/bevodokate"
    )


@UserBot.on_message(filters.command(["ht"], ".") & filters.me)
async def heads_tails(_, message: Message):
    coin_sides = ["Heads", "Tails"]
    ht = f"Heads or Tails? `{choice(coin_sides)}`"
    await message.edit(ht)


@UserBot.on_message(filters.command("reverset", ".") & filters.me)
async def text_reverse(_, message: Message):
    cmd = message.command

    reverse_text = ""
    if len(cmd) > 1:
        reverse_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        reverse_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Give me something to reverse`"[::-1])
        await asyncio.sleep(2)
        await message.delete()
        return

    await message.edit(reverse_text[::-1])


@UserBot.on_message(filters.me & filters.command(["shg", "shrug"], "."))
async def shrug(_, message):
    await message.edit(random.choice(MEMES.SHRUGS))


@UserBot.on_message(filters.me & filters.command("flip", "."))
async def flip_text(_, message):
    cmd = message.command

    text = ""
    if len(cmd) > 1:
        text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Give me something to reverse`"[::-1])
        await asyncio.sleep(2)
        await message.delete()
        return

    final_str = ""
    for char in text:
        if char in MEMES.REPLACEMENT_MAP.keys():
            new_char = MEMES.REPLACEMENT_MAP[char]
        else:
            new_char = char
        final_str += new_char
    if text != final_str:
        await message.edit(final_str)
    else:
        await message.edit(text)


# Command help section
add_command_help(
    "text",
    [
        [".nice", "Replaces command with NICENICENICENICE."],
        [".compliment", "Replaces command with a nice compliment."],
        [".devexcuse", "Replaces command with an excuse that a developer would give."],
        [".reverse", "Sends ASCII version of the Uno reverse card."],
        [
            ".slap",
            "Sends a randomly generated slap text. Can become very random at some times.",
        ],
        [
            ".insult",
            "Sends a randomly generated insult. Can become very random at some times.",
        ],
        [".vapor", "Vaporizes the text."],
        [".weeb `or` .weebify", "Weebifies the text."],
        [".ok", "Sends -_____- with a fast animation."],
        ["-_-", "Extends to -________-"],
        [".f", "Pay respects"],
        [".F", "Pay respects but filled"],
        ["#f", "Pay respects but calligraphy."],
        [".mockt", "Mock (text only version)"],
        [".dice", "Send dice animation"],
        [".target", "Send target animation"],
        ["oof", "Oof"],
        [";_; `or` .sad `or` cri", ";_;"],
        [".ht", "Heads or Tails"],
        [".reverset", "Reverses the text"],
        [".shrug", "Random shrug"],
    ],
)
