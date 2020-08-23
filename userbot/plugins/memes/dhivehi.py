from pyrogram import Filters, Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

dhivehi_text_memes = {
    'bidi': {'meme': "🚬", 'help': 'Bidi'},
    '100': {'meme': "💯", 'help': '💯'},
    'kada': {'alts': ['k'], 'meme': "ކަޑަ؟", 'help': "ކަޑަ؟"},
    'blk': {'alts': ['b'], 'meme': "ޭބަލާކ", 'help': 'ޭބަލާކ'},
    'gerey': {'alts': ['g'], 'meme': "ގެރޭ", 'help': "ގެރޭ"},
    'ngb': {'alts': ['n'], 'meme': "ނަގޫބަޅާ", 'help': "ނަގޫބަޅާ"},
    'amf': {'alts': ['a'], 'meme': "އަމާފޫޅު", 'help': "އަމާފޫޅު"},
    'fdb': {'alts': [], 'meme': "ފަޑަބޮއެ", 'help': "ފަޑަބޮއެ"},
    'kg': {'alts': [], 'meme': "ކަލޯގަޔާ", 'help': "ކަލޯގަޔާ"},
}

dhivehi_text_memes_commands = []
fixed_memes_help = []
for dv in dhivehi_text_memes:
    dhivehi_text_memes_commands.append(dv)
    if 'alts' in dhivehi_text_memes[dv]:
        for y in dhivehi_text_memes[dv]['alts']:
            dhivehi_text_memes_commands.append(y)

    # Construct the help from the same loop eh.
    command = f'.{dv}'
    if 'alts' in dhivehi_text_memes[dv]:
        for y in dhivehi_text_memes[dv]['alts']:
            command += f' __or__ .{y}'
    fixed_memes_help.append([command, dhivehi_text_memes[dv]['help']])


@UserBot.on_message(Filters.command(dhivehi_text_memes_commands, ".") & Filters.me)
async def dhivehi_memes(_, message: Message):
    cmd = message.command[0]
    if cmd not in dhivehi_text_memes:
        for x in dhivehi_text_memes:
            if 'alts' in dhivehi_text_memes[x] and cmd in dhivehi_text_memes[x]['alts']:
                meme = dhivehi_text_memes[x]
                break
    else:
        meme = dhivehi_text_memes[message.command[0]]

    await message.edit(meme['meme'])


# Command help section
add_command_help(
    'dhivehi', fixed_memes_help
)
