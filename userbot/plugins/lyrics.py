import asyncio

from pyrogram import Filters, Message

from userbot import UserBot
from userbot import ALLOWED_USERS
from userbot.plugins.help import add_command_help


@UserBot.on_message(Filters.command(['l', 'lyrics'], ".") & (Filters.me | Filters.user(ALLOWED_USERS)))
async def send_lyrics(bot: UserBot, message: Message):
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

        await message.edit(f"Getting lyrics for `{song_name}`")
        lyrics_results = await bot.get_inline_bot_results("ilyricsbot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await bot.send_inline_bot_result(
                chat_id="me",
                query_id=lyrics_results.query_id,
                result_id=lyrics_results.results[0].id,
                hide_via=True)
            await asyncio.sleep(2)
            
            lyrics = saved.updates[1].message.message.split("\n\n")
            for lyric in lyrics[:-1]:
                if lyric == "":
                    pass
                await bot.send_messages(chat_id=message.chat.id, lyric) 

            # forward from Saved Messages
            #await bot.forward_messages(
            #    chat_id=message.chat.id,
            #    from_chat_id="me",
            #    message_ids=saved.updates[1].message.id,
            #    as_copy=True
            #)
            # delete the message from Saved Messages
            await bot.delete_messages("me", saved.updates[1].message.id)
        except TimeoutError:
            await message.edit("That didn't work out")
            await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        print(e)
        await message.edit("`Failed to find lyrics`")
        await asyncio.sleep(2)
        await message.delete()


# Command help section
add_command_help(
    'lyrics', [
        ['.l `or` .lyrics', 'Search lyrics and send.']
    ]
)
