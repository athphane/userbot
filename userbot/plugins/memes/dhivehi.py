from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

dhivehi_text_memes = {
    'bidi': {'meme': "🚬", 'help': 'Bidi'},
    'kada': {'alts': ['k'], 'meme': "ކަޑަ؟", 'help': "ކަޑަ؟"},
    'gerey': {'alts': ['g'], 'meme': "ގެރޭ", 'help': "ގެރޭ"}
}

dhivehi_text_memes_commands = []
for x in dhivehi_text_memes:
    dhivehi_text_memes_commands.append(x)
    if 'alts' in dhivehi_text_memes[x]:
        for y in dhivehi_text_memes[x]['alts']:
            dhivehi_text_memes_commands.append(y)


@UserBot.on_message(Filters.command(dhivehi_text_memes_commands, ".") & Filters.me)
async def dhivehi_memes(_, message: Message):
    command = message.command[0]
    if command not in dhivehi_text_memes:
        for x in dhivehi_text_memes:
            if 'alts' in dhivehi_text_memes[x] and command in dhivehi_text_memes[x]['alts']:
                meme = dhivehi_text_memes[x]
                break
    else:
        meme = dhivehi_text_memes[message.command[0]]

    await message.edit(meme['meme'])


# Command help section
fixed_memes_help = []
for x in dhivehi_text_memes:
    command = f'.{x}'
    if 'alts' in dhivehi_text_memes[x]:
        for y in dhivehi_text_memes[x]['alts']:
            command += f' __or__ .{y}'
    fixed_memes_help.append([command, dhivehi_text_memes[x]['help']])

add_command_help(
    'dhivehi', fixed_memes_help
)
