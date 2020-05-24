from pyrogram import Filters, Message, Emoji

from userbot import UserBot
from userbot.helpers.file_sending_helpers import send_saved_image, send_saved_animation
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command("fast", ".") & Filters.me)
async def fast(bot: UserBot, message: Message):
    await message.delete()
    await send_saved_image(bot, message, "fast_image", "fast.jpg", caption="I. Am. Speed.")


@UserBot.on_message(Filters.command(['tfb', 'tbf'], ".") & Filters.me)
async def tfb(bot: UserBot, message: Message):
    await message.delete()
    await send_saved_image(bot, message, "tfb_image", "tfb.jpg")


@UserBot.on_message(Filters.command("kill", ".") & Filters.me)
async def kill(bot: UserBot, message: Message):
    await message.delete()
    await send_saved_animation(bot, message, "kill_image", "killua.gif", caption="I will kill you.")


@UserBot.on_message(Filters.command("lust", ".") & Filters.me)
async def kill(bot: UserBot, message: Message):
    await message.delete()
    await send_saved_animation(bot, message, "lust_gif", "lust.gif",
                               caption=f"I wanna do bad things with you {Emoji.SMIRKING_FACE}")


@UserBot.on_message(Filters.command("dmf", ".") & Filters.me)
async def dmf(bot: UserBot, message: Message):
    await send_saved_animation(bot, message, "dmf_image", "dmf.gif")
    await message.delete()


@UserBot.on_message(Filters.command(['smart', 'intelligence'], ".") & Filters.me)
async def smart(bot: UserBot, message: Message):
    await send_saved_image(bot, message, "intelligence_image", "intelligence.jpg")
    await message.delete()


@UserBot.on_message(Filters.command("sobimin", ".") & Filters.me)
async def sob_im_in(bot: UserBot, message: Message):
    await message.delete()
    await send_saved_image(bot, message, "sob_im_in_image", "sob_im_in.jpg")


# Command help section
add_command_help(
    'pictures', [
        ['.fast', 'Picture of Lightning McQueen and says "I am speed.'],
        ['.tfb', 'Some guy saying "Tha Fuah Balhaa". This was an inside joke at Baivaru but now in this userbot.'],
        ['.kill', 'Gif of Killua from HunterXHunter with caption "I will kill you"'],
        ['.lust', 'Gif of lustful things.'],
        ['.dmf', 'Syndrome from The Incredible\'s saying "You dense motherfucker".'],
        ['.smart', 'Press E to use intelligence.'],
        ['.sobimin', "Morty - SOB I'm In"]
    ]
)
