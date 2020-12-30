from pyrogram import filters, emoji
from pyrogram.types import Message
from userbot import UserBot
from userbot.helpers.file_sending_helpers import send_saved_image, send_saved_animation
from userbot.plugins.help import add_command_help

memes_data = {
    "fast": {
        "name": "fast_image",
        "image": "fast.jpg",
        "type": "image",
        "caption": "I. Am. Speed.",
        "help": "Picture of Lightning McQueen and says 'I am speed'",
    },
    "tfb": {
        "alts": ["tbf"],
        "name": "tfb_image",
        "image": "tfb.jpg",
        "type": "image",
        "caption": None,
        "help": "Some guy saying 'The Fuah Balhaa'",
    },
    "kill": {
        "name": "kill_image",
        "image": "killua.gif",
        "type": "animation",
        "caption": "I will kill you.",
        "help": "Gif of Killua from Hunter X Hunter.",
    },
    "lust": {
        "name": "lust_gif",
        "image": "lust.gif",
        "type": "animation",
        "caption": f"I wanna do bad things with you {emoji.SMIRKING_FACE}",
        "help": "Gif of lustful things.",
    },
    "dmf": {
        "name": "dmf_image",
        "image": "dmf.gif",
        "type": "animation",
        "caption": None,
        "help": 'Syndrome from The Incredible\'s saying "You dense mf".',
    },
    "smart": {
        "alts": ["intelligence"],
        "name": "intelligence_image",
        "image": "intelligence.jpg",
        "type": "image",
        "caption": None,
        "help": "Press E to use intelligence.",
    },
    "sobimin": {
        "name": "sob_im_in_image",
        "image": "sob_im_in.jpg",
        "type": "image",
        "caption": None,
        "help": "Morty - SOB I'm In",
    },
    "omg": {
        "name": "omg_image",
        "image": "omg.gif",
        "type": "animation",
        "caption": None,
        "help": "Anime character saying OMG.",
    },
    "ma": {
        "name": "ma_image",
        "image": "ma.JPG",
        "type": "image",
        "caption": None,
        "help": "Anime character saying mashaallah.",
    },
    "sa": {
        "name": "sa_image",
        "image": "sa.JPG",
        "type": "image",
        "caption": None,
        "help": "Anime character saying subuhanallah.",
    },
    "al": {
        "name": "al_image",
        "image": "al.JPG",
        "type": "image",
        "caption": None,
        "help": "Anime character saying alhamdhulilah.",
    },
    "astf": {
        "name": "astf_image",
        "image": "astf.JPG",
        "type": "image",
        "caption": None,
        "help": "Anime character saying asthagfirullah.",
    },
    "ia": {
        "name": "ia_image",
        "image": "ia.JPG",
        "type": "image",
        "caption": None,
        "help": "Anime character inshaallah.",
    },
    "dumb": {
        "name": "dumb",
        "image": "dumb.jpg",
        "type": "image",
        "caption": None,
        "help": "Are you dumb?.",
    },
}

memes = []
fixed_memes_help = []
for meme in memes_data:
    memes.append(meme)
    if "alts" in memes_data[meme]:
        for y in memes_data[meme]["alts"]:
            memes.append(y)

    # Construct the help from the same loop eh.
    command = f".{meme}"
    if "alts" in memes_data[meme]:
        for y in memes_data[meme]["alts"]:
            command += f" __or__ .{y}"
    fixed_memes_help.append([command, memes_data[meme]["help"]])


@UserBot.on_message(filters.command(memes, ".") & filters.me)
async def fixed_memes(_, message: Message):
    await message.delete()

    cmd = message.command[0]
    if cmd not in memes_data:
        for x in memes_data:
            if "alts" in memes_data[x] and cmd in memes_data[x]["alts"]:
                the_meme = memes_data[x]
                break
    else:
        the_meme = memes_data[message.command[0]]

    if the_meme["type"] == "animation":
        await send_saved_animation(
            message, the_meme["name"], the_meme["image"], caption=the_meme["caption"]
        )
    elif the_meme["type"] == "image":
        await send_saved_image(
            message, the_meme["name"], the_meme["image"], caption=the_meme["caption"]
        )


# Command help section
add_command_help("memes", fixed_memes_help)
