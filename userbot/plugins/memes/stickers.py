from time import sleep
from userbot import UserBot
from pyrogram import Filters, Message
from userbot.helpers.PyroHelpers import ReplyCheck
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command("mock", ".") & Filters.me)
async def mock_people(bot: UserBot, message: Message):
    cmd = message.command

    mock_text = ""
    if len(cmd) > 1:
        mock_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        mock_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        await message.edit("gIvE sOMEtHInG tO MoCk")
        sleep(2)
        await message.delete()
        return

    mock_results = await bot.get_inline_bot_results(
        "stickerizerbot",
        "#7" + mock_text)

    try:
        await bot.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=mock_results.query_id,
            result_id=mock_results.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        await message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)

    await message.delete()


@UserBot.on_message(Filters.command("animegirl", ".") & Filters.me)
async def anime_girl(bot: UserBot, message: Message):
    cmd = message.command

    anime_girl_text = ""
    if len(cmd) > 1:
        anime_girl_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        anime_girl_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        await message.edit("`Senpai I need something to say :(`")
        sleep(2)
        await message.delete()
        return

    anime_girl_results = await bot.get_inline_bot_results(
        "stickerizerbot",
        "#32" + anime_girl_text)

    try:
        await bot.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=anime_girl_results.query_id,
            result_id=anime_girl_results.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        await message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)
    await message.delete()


@UserBot.on_message(Filters.command("animeboy", ".") & Filters.me)
async def anime_boy(bot: UserBot, message: Message):
    cmd = message.command

    anime_boy_text = ""
    if len(cmd) > 1:
        anime_boy_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) is 1:
        anime_boy_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) is 1:
        await message.edit("`Senpai I need something to say :(`")
        sleep(2)
        await message.delete()
        return

    anime_girl_results = await bot.get_inline_bot_results(
        "stickerizerbot",
        "#37" + anime_boy_text)

    try:
        await bot.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=anime_girl_results.query_id,
            result_id=anime_girl_results.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        await message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)
    await message.delete()


@UserBot.on_message(Filters.command("ggl", ".") & Filters.me)
async def google_sticker(bot: UserBot, message: Message):
    await message.delete()
    cmd = message.command

    ggl_text = ""
    if len(cmd) > 1:
        ggl_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        ggl_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("I need something to google")
        sleep(2)
        await message.delete()
        return

    ggl_result = await bot.get_inline_bot_results(
        "stickerizerbot",
        "#12" + ggl_text)
    try:
        await bot.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=ggl_result.query_id,
            result_id=ggl_result.results[0].id,
            reply_to_message_id=ReplyCheck(message),
            hide_via=True)
    except TimeoutError:
        await message.edit("@StickerizerBot didn't respond in time.")
        sleep(2)
        await message.delete()


# Command help section
add_command_help(
    'stickers', [
        ['.mock', 'Sends a Spongebob mocking meme of what you sent with command or text of what you replied to.\n'
                  '**Usage**:\n```.mock you smell like shit``` will give you the meme that says "You smell like shit"\n'
                  'Reply to a text message with .mock and it will grab the text of that message and generate the meme.'
         ],
        ['.animegirl', 'Sends an anime girl with a card of what you want. Rules apply as above.'],
        ['.animeboy', 'Sends an anime boy with a card of what you want. Rules apply as above.'],
        ['.ggl', 'Sends google search buttons with the query you give it.. Rules apply as above.'],
    ]
)
