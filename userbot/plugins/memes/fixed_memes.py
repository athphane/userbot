from pyrogram import Filters, Message, Emoji

from userbot import UserBot
from userbot.helpers.file_sending_helpers import send_saved_image, send_saved_animation
from userbot.plugins.help import add_command_help

memes_data = {
    'fast': {'name': 'fast_image', 'image': 'fast.jpg', 'type': 'image', 'caption': 'I. Am. Speed.',
             'help': 'Picture of Lightning McQueen and says \'I am speed\''},
    'tfb': {'alts': ['tbf'], 'name': 'tfb_image', 'image': 'tfb.jpg', 'type': 'image', 'caption': None,
            'help': 'Some guy saying \'The Fuah Balhaa\''},
    'kill': {'name': 'kill_image', 'image': 'killua.gif', 'type': 'animation', 'caption': 'I will kill you.',
             'help': 'Gif of Killua from Hunter X Hunter.'},
    'lust': {'name': 'lust_gif', 'image': 'lust.gif', 'type': 'animation',
             'caption': f"I wanna do bad things with you {Emoji.SMIRKING_FACE}", 'help': 'Gif of lustful things.'},
    'dmf': {'name': 'dmf_image', 'image': 'dmf.gif', 'type': 'animation', 'caption': None,
            'help': 'Syndrome from The Incredible\'s saying "You dense motherfucker".'},
    'smart': {'name': 'intelligence_image', 'image': 'intelligence.jpg', 'type': 'image', 'caption': None,
              'help': 'Press E to use intelligence.'},
    'intelligence': {'name': 'intelligence_image', 'image': 'intelligence.jpg', 'type': 'image', 'caption': None,
                     'help': 'Press E to use intelligence.'},
    'sobimin': {'name': 'sob_im_in_image', 'image': 'sob_im_in.jpg', 'type': 'image', 'caption': None,
                'help': 'Morty - SOB I\'m In'},
}

# memes = [x for x in memes_data]
memes = []
for x in memes_data:
    memes.append(x)

    if 'alts' in memes_data[x]:
        for y in memes_data[x]['alts']:
            memes.append(y)


@UserBot.on_message(Filters.command(memes, ".") & Filters.me)
async def fixed_memes(bot: UserBot, message: Message):
    command = message.command[0]
    if command not in memes_data:
        for x in memes_data:
            if 'alts' in memes_data[x] and command in memes_data[x]['alts']:
                meme = memes_data[x]
                break
    else:
        meme = memes_data[message.command[0]]

    await message.delete()
    if meme['type'] == 'animation':
        await send_saved_animation(bot, message, meme['name'], meme['image'], caption=meme['caption'])
    elif meme['type'] == 'image':
        await send_saved_image(bot, message, meme['name'], meme['image'], caption=meme['caption'])


# Command help section
fixed_memes_help = []
for x in memes_data:
    command = f'.{x}'
    if 'alts' in memes_data[x]:
        for y in memes_data[x]['alts']:
            command += f' __or__ .{y}'
    fixed_memes_help.append([command, memes_data[x]['help']])

add_command_help(
    'memes', fixed_memes_help
)
