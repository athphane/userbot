import asyncio

from pyrogram import filters
from pyrogram.types import Message
from userbot import UserBot, ALLOWED_USERS
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command(['m', 'music'], ".") & (filters.me | filters.user(ALLOWED_USERS)))
async def send_music(_, message: Message):
    try:
        cmd = message.command

        song_name = ""
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message and len(cmd) == 1:
            song_name = message.reply_to_message.text or message.reply_to_message.caption
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit("Give a song name")
            await asyncio.sleep(2)
            await message.delete()
            return

        song_results = await UserBot.get_inline_bot_results("deezermusicbot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await UserBot.send_inline_bot_result(
                chat_id="me",
                query_id=song_results.query_id,
                result_id=song_results.results[0].id,
                hide_via=True)

            # forward as a new message from Saved Messages
            saved = await UserBot.get_messages("me", int(saved.updates[1].message.id))
            reply_to = message.reply_to_message.message_id if message.reply_to_message else None
            await UserBot.send_audio(
                chat_id=message.chat.id,
                audio=str(saved.audio.file_id),
                file_ref=str(saved.audio.file_ref),
                reply_to_message_id=reply_to
            )

            # delete the message from Saved Messages
            await UserBot.delete_messages("me", saved.message_id)
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
