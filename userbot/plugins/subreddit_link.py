from pyrogram import Filters, Message
from userbot import BOT
from userbot.helpers.PyroHelpers import GetChatID, ReplyCheck

the_regex = "^r\/([^\s\/])+"


# Generate full Reddit link with subreddit
@BOT.on_message(Filters.regex(the_regex) & Filters.me)
def subreddit_link(bot: BOT, message: Message):
    html = "<a href='{link}'>{string}</a>"
    message.delete()
    BOT.send_message(
        GetChatID(message),
        html.format(link="https://reddit.com/" + message.text, string=message.text),
        disable_web_page_preview=True,
        reply_to_message_id=ReplyCheck(message)
    )
