import asyncio

from pyrogram import Filters, Message

from userbot import UserBot
from userbot import ALLOWED_USERS
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['m', 'music'], ".") & (Filters.me | Filters.user(ALLOWED_USERS)))
async def send_music(bot: UserBot, message: Message):
    try:
        cmd = message.command

        song_name = ""
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message and len(cmd) == 1:
            song_name = message.reply_to_message.text
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit("Give a song name")
            await asyncio.sleep(2)
            await message.delete()
            return

        song_results = await bot.get_inline_bot_results("deezermusicbot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await bot.send_inline_bot_result(
                chat_id="me",
                query_id=song_results.query_id,
                result_id=song_results.results[0].id,
                hide_via=True)

            # forward from Saved Messages
            reply_to = message.reply_to_message.message_id
            await bot.send_audio (
                chat_id=message.chat.id,
                audio=saved.updates[1].media.document.id,
                file_ref=saved.updates[1].media.document.file_reference,
                reply_to_message_id=reply_to
            )
#             await bot.forward_messages(
#                 chat_id=message.chat.id,
#                 from_chat_id="me",
#                 message_ids=saved.updates[1].message.id,
#                 as_copy=True
#             )

            # delete the message from Saved Messages
            await bot.delete_messages("me", saved.updates[1].message.id)
        except TimeoutError:
            await message.edit("That didn't work out")
            await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        print(e)
        await message.edit("`Failed to find song`")
        await asyncio.sleep(2)
        await message.delete()


# Command help section
add_command_help(
    'music', [
        ['.m `or` .music', 'Search songs and send.']
    ]
)
