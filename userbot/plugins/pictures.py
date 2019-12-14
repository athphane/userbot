from pyrogram import Filters, Message
from userbot import UserBot
from userbot.helpers.file_sending_helpers import send_saved_image, send_saved_animation


@UserBot.on_message(Filters.command("fast", ".") & Filters.me)
async def fast(bot: UserBot, message: Message):
    await message.edit("Gotta go fast")
    await send_saved_image(message, "fast_image", "fast.jpg")


@UserBot.on_message(Filters.command(['tfb', 'tbf'], ".") & Filters.me)
async def tfb(bot: UserBot, message: Message):
    await send_saved_image(message, "tfb_image", "tfb.jpg")
    await message.delete()


@UserBot.on_message(Filters.command("kill", ".") & Filters.me)
async def kill(bot: UserBot, message: Message):
    await message.edit("I will kill you")
    await send_saved_animation(message, "kill_image", "killua.gif")


@UserBot.on_message(Filters.command("dmf", ".") & Filters.me)
async def dmf(bot: UserBot, message: Message):
    await send_saved_animation(message, "dmf_image", "dmf.gif")
    await message.delete()


@UserBot.on_message(Filters.command(['smart', 'intelligence'], ".") & Filters.me)
async def smart(bot: UserBot, message: Message):
    await send_saved_image(message, "intelligence_image", "intelligence.jpg")
    await message.delete()
