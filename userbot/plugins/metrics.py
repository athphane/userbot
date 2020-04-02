from userbot import UserBot
from pyrogram import Filters, Message

from userbot.plugins.help import add_command_help


class Custom(dict):
    def __missing__(self, key):
        return 0


@UserBot.on_message(Filters.command("wordcount", ".") & Filters.me)
async def word_count(bot: UserBot, message: Message):
    await message.delete()
    words = Custom()
    progress = await bot.send_message(message.chat.id, "`Processed 0 messages...`")
    total = 0
    async for msg in bot.iter_history(message.chat.id, 1000):
        total += 1
        if total % 100 == 0:
            await progress.edit_text(f"`Processed {total} messages...`")
        if msg.text:
            for word in msg.text.split():
                words[word.lower()] += 1
        if msg.caption:
            for word in msg.caption.split():
                words[word.lower()] += 1
    freq = sorted(words, key=words.get, reverse=True)
    out = "Word Counter\n"
    for i in range(25):
        out += f"{i + 1}. {words[freq[i]]}: {freq[i]}\n"

    await progress.edit_text(out, parse_mode=None)

# Command help section
add_command_help(
    'metrics', [
        ['.wordcount', 'Finds the 25 most used words in the last 1000 messages in a group or private chat. Use in '
                       'chat you want to find the metric in.'],
    ]
)
