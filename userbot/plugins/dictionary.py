import asyncio
from html import escape
from typing import Any
from urllib.parse import quote

import aiohttp
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import LinkPreviewOptions, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

API_URL = "https://freedictionaryapi.com/api/v1/entries/en/{word}"
TIMEOUT = aiohttp.ClientTimeout(total=10)
MAX_SENSES = 5
MAX_LENGTH = 4096


async def fetch_entries(word: str) -> dict[str, Any]:
    """Return the Free Dictionary API response for an English word."""
    url = API_URL.format(word=quote(word, safe=""))
    async with (
        aiohttp.ClientSession(timeout=TIMEOUT) as session,
        session.get(url) as resp,
    ):
        resp.raise_for_status()
        return await resp.json(content_type=None)


def format_entries(data: dict[str, Any]) -> str:
    """Render API entries as Telegram HTML, or an empty string if none exist."""
    entries = data.get("entries") or []
    if not entries:
        return ""

    parts = [f"<b>{escape(data.get('word', ''))}</b>"]
    for entry in entries:
        block = [f"<b><i>{escape(entry.get('partOfSpeech', 'word').title())}</i></b>"]
        ipa = next(
            (p["text"] for p in entry.get("pronunciations", []) if p.get("type") == "ipa"),
            None,
        )
        if ipa:
            block[0] += f"  <code>{escape(ipa)}</code>"

        senses = entry.get("senses", [])
        for index, sense in enumerate(senses[:MAX_SENSES], 1):
            block.append(f"{index}. {escape(sense.get('definition', ''))}")
            if sense.get("examples"):
                block.append(f"    <i>“{escape(sense['examples'][0])}”</i>")
        if len(senses) > MAX_SENSES:
            block.append(f"<i>…and {len(senses) - MAX_SENSES} more</i>")

        for label in ("synonyms", "antonyms"):
            if entry.get(label):
                block.append(f"<b>{label.title()}:</b> {escape(', '.join(entry[label]))}")
        parts.append("\n".join(block))

    source = (data.get("source") or {}).get("url")
    if source:
        href = escape(quote(source, safe=":/%#?=&"), quote=True)
        footer = f'\n\n<a href="{href}">Wiktionary</a>'
    else:
        footer = ""
    body = "\n\n".join(parts)
    if len(body) + len(footer) > MAX_LENGTH:
        cut = MAX_LENGTH - len(footer) - 1
        body = body[:cut].rsplit("\n", 1)[0] + "\n…"
    return body + footer


@UserBot.on_message(filters.command(["define", "dict"], ".") & filters.me)
async def define(bot: UserBot, message: Message):
    """Define the word given as an argument or in the replied-to message."""
    cmd = message.command or []
    if len(cmd) > 1:
        word = " ".join(cmd[1:])
    elif message.reply_to_message and message.reply_to_message.text:
        word = message.reply_to_message.text
    else:
        await message.edit("`Can't pass to the void.`")
        await asyncio.sleep(2)
        await message.delete()
        return

    word = word.strip()
    try:
        data = await fetch_entries(word)
    except (aiohttp.ClientError, TimeoutError, ValueError) as e:
        print(e)
        await message.edit(
            "`The dictionary API is unreachable right now. Try again later.`"
        )
        return

    output = format_entries(data)
    if not output:
        await message.edit(
            f"No definition found for <b>{escape(word)}</b>.",
            parse_mode=ParseMode.HTML,
        )
        return
    await message.edit(
        output,
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


# Command help section
add_command_help(
    "dictionary",
    [
        [".define | .dict", "Define the word you send or reply to."],
    ],
)
