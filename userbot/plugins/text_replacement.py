import re

import pyrogram.enums
from pyrogram import filters
from pyrogram.types import Message, LinkPreviewOptions

from userbot import UserBot
from userbot.plugins.help import add_command_help

subreddit_regex = r"^r\/([^\s\/])+"


# Generate full Reddit link with subreddit
@UserBot.on_message(filters.regex(subreddit_regex) & filters.me)
async def subreddit_link(bot: UserBot, message: Message):
    html = "<a href='{link}'>{string}</a>"
    await message.edit(
        html.format(link="https://reddit.com/" + message.text, string=message.text),
        disable_web_page_preview=True,
        parse_mode=pyrogram.enums.ParseMode.HTML,
    )


# Assuming UserBot is your Client instance
twitter_regex = r'https?://(www\.)?(twitter\.com|x\.com)/[^\s]+'


@UserBot.on_message(filters.regex(twitter_regex) & filters.me)
async def twitter_url_fixer(bot: UserBot, message: Message):
    # Extract the text from the message
    message_text = message.text

    # Check and replace twitter.com or x.com with fxtwitter.com
    modified_text = re.sub(r'(https?://)(twitter\.com|x\.com)', r'\1fxtwitter.com', message_text)

    # Edit the message with the modified link
    await message.edit(
        modified_text,
        link_preview_options=LinkPreviewOptions(show_above_text=True)
    )


# Assuming UserBot is your Client instance
instagram_regex = r'https?://(www\.)?instagram\.com/[^\s]+'

@UserBot.on_message(filters.regex(instagram_regex) & filters.me)
async def instagram_url_fixer(bot: UserBot, message: Message):
    # Extract the text from the message
    message_text = message.text

    if "www.instagram.com" in message_text:
        message_text = message_text.replace("www.instagram.com", "instagram.com")

    if "instagram.com" in message_text:
        message_text = message_text.replace("instagram.com", "ddinstagram.com")

    if '?' in message_text:
        message_text = message_text.split('?')[0]

    await message.delete()

    await bot.send_message(
        message.chat.id,
        message_text,
        link_preview_options=LinkPreviewOptions(show_above_text=True)
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
            "fxtwitter.com.",
        ],
    ],
)
