from pyrogram import Filters, Message, Emoji

from userbot import UserBot
from userbot.helpers.file_sending_helpers import send_saved_image, send_saved_animation
from userbot.plugins.help import add_command_help

memes_data = {
    'fast': {'name': 'fast_image', 'image': 'fast.jpg', 'type': 'image', 'caption': 'I. Am. Speed.'},
    'tfb': {'name': 'tfb_image', 'image': 'tfb.jpg', 'type': 'image', 'caption': None},
    'tbf': {'name': 'tfb_image', 'image': 'tfb.jpg', 'type': 'image', 'caption': None},
    'kill': {'name': 'kill_image', 'image': 'killua.gif', 'type': 'animation', 'caption': 'I will kill you.'},
    'lust': {'name': 'lust_gif', 'image': 'lust.gif', 'type': 'animation',
             'caption': f"I wanna do bad things with you {Emoji.SMIRKING_FACE}"},
    'dmf': {'name': 'dmf_image', 'image': 'dmf.gif', 'type': 'animation', 'caption': None},
    'smart': {'name': 'intelligence_image', 'image': 'intelligence.jpg', 'type': 'image', 'caption': None},
    'intelligence': {'name': 'intelligence_image', 'image': 'intelligence.jpg', 'type': 'image', 'caption': None},
    'sobimin': {'name': 'sob_im_in_image', 'image': 'sob_im_in.jpg', 'type': 'image', 'caption': None},
}

memes = [x for x in memes_data]


@UserBot.on_message(Filters.command(memes, ".") & Filters.me)
async def fixed_memes(bot: UserBot, message: Message):
    meme = memes_data[message.command[0]]
    await message.delete()
    if meme['type'] == 'animation':
        await send_saved_animation(bot, message, meme['name'], meme['image'], caption=meme['caption'])
    elif meme['type'] == 'image':
        await send_saved_image(bot, message, meme['name'], meme['image'], caption=meme['caption'])


# Command help section
add_command_help(
    'memes', [
        ['.fast', 'Picture of Lightning McQueen and says "I am speed.'],
        ['.tfb', 'Some guy saying "Tha Fuah Balhaa". This was an inside joke at Baivaru but now in this userbot.'],
        ['.kill', 'Gif of Killua from HunterXHunter with caption "I will kill you"'],
        ['.lust', 'Gif of lustful things.'],
        ['.dmf', 'Syndrome from The Incredible\'s saying "You dense motherfucker".'],
        ['.smart', 'Press E to use intelligence.'],
        ['.sobimin', "Morty - SOB I'm In"]
    ]
)
