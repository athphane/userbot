import asyncio
from html import escape
from typing import Any
from urllib.parse import quote

import aiohttp
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

try:
    from pyrogram.types import LinkPreviewOptions
except ImportError:
    class LinkPreviewOptions:
        def __init__(self, is_disabled: bool = False, show_above_text: bool = False):
            self.is_disabled = is_disabled
            self.show_above_text = show_above_text

from userbot import UserBot
from userbot.plugins.help import add_command_help

API_URL = "https://freedictionaryapi.com/api/v1/entries/en/{word}"
TIMEOUT = aiohttp.ClientTimeout(total=10)
MAX_SENSES = 5
MAX_LENGTH = 4096


def render_html(parts: list[tuple[str, str, str]], footer: str) -> str:
    """Limit escaped text without splitting HTML tags, entities, or UTF-16 pairs."""
    remaining = MAX_LENGTH - len(footer.encode("utf-16-le")) // 2 - 1
    output = []
    for prefix, text, suffix in parts:
        fragment = prefix + escape(text) + suffix
        size = len(fragment.encode("utf-16-le")) // 2
        if size <= remaining:
            output.append(fragment)
            remaining -= size
            continue

        budget = remaining - len((prefix + suffix).encode("utf-16-le")) // 2
        if budget >= 0:
            clipped = []
            for char in text:
                escaped = escape(char)
                size = len(escaped.encode("utf-16-le")) // 2
                if size > budget:
                    break
                clipped.append(escaped)
                budget -= size
            output.append(prefix + "".join(clipped) + suffix)
        output.append("…")
        break
    return "".join(output) + footer


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

    parts = [("<b>", data.get("word", ""), "</b>")]
    for entry in entries:
        parts.append(
            ("\n\n<b><i>", entry.get("partOfSpeech", "word").title(), "</i></b>")
        )
        ipa = next(
            (
                p["text"]
                for p in entry.get("pronunciations", [])
                if p.get("type") == "ipa"
            ),
            None,
        )
        if ipa:
            parts.append(("  <code>", ipa, "</code>"))

        senses = entry.get("senses", [])
        for index, sense in enumerate(senses[:MAX_SENSES], 1):
            parts.append((f"\n{index}. ", sense.get("definition", ""), ""))
            if sense.get("examples"):
                parts.append(("\n    <i>“", sense["examples"][0], "”</i>"))
        if len(senses) > MAX_SENSES:
            parts.append(("\n<i>", f"…and {len(senses) - MAX_SENSES} more", "</i>"))

        for label in ("synonyms", "antonyms"):
            if entry.get(label):
                parts.append(
                    (f"\n<b>{label.title()}:</b> ", ", ".join(entry[label]), "")
                )

    footer = (
        '\n\nVia <a href="https://freedictionaryapi.com/">FreeDictionaryAPI.com</a>'
    )
    source = (data.get("source") or {}).get("url")
    if source:
        href = escape(quote(source, safe=":/%#?=&"), quote=True)
        footer += f' · <a href="{href}">Wiktionary</a>'
    return render_html(parts, footer)


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
