import re
from urllib.parse import urlsplit, urlunsplit

import pyrogram.enums
from pyrogram import filters
from pyrogram.types import LinkPreviewOptions, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

subreddit_regex = r"^r\/([^\s\/])+"


# Generate full Reddit link with subreddit
@UserBot.on_message(filters.regex(subreddit_regex) & filters.me)
async def subreddit_link(bot: UserBot, message: Message):
    html = "<a href='{link}'>{string}</a>"
    await message.edit(
        html.format(link="https://reddit.com/" + message.text, string=message.text),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        parse_mode=pyrogram.enums.ParseMode.HTML,
    )


twitter_regex = re.compile(
    r"https?://(?:www\.|mobile\.)?(?:twitter\.com|x\.com)/[^\s<>\"']+",
    re.IGNORECASE,
)


def clean_twitter_url(match: re.Match) -> str:
    """Convert a Twitter URL and remove its query without consuming punctuation."""
    original = match.group(0)
    url = original.rstrip(".,!;:)]}")
    punctuation = original[len(url) :]
    parts = urlsplit(url)
    return urlunsplit(parts._replace(netloc="fxtwitter.com", query="")) + punctuation


@UserBot.on_message(filters.regex(twitter_regex) & filters.me)
async def twitter_url_fixer(bot: UserBot, message: Message) -> None:
    """Replace outgoing Twitter/X links with clean FxTwitter links."""
    modified_text = twitter_regex.sub(clean_twitter_url, message.text)
    await message.edit(
        modified_text,
        link_preview_options=LinkPreviewOptions(show_above_text=True),
    )

# Command help section
add_command_help(
    "reddit",
    [
        [
            "r/telegram",
            "As long as your message starts with r/, it will automatically generate a subreddit link and "
            "hyperlink your message.",
        ],
    ],
)

add_command_help(
    "twitter",
    [
        [
            "https://twitter.com/username",
            "If the message contains a Twitter link, it will automatically replace twitter.com or x.com with "
            "fxtwitter.com and remove query parameters (including share tracking).",
        ],
    ],
)
