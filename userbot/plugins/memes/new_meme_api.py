from pyrogram import emoji, filters
from pyrogram.types import Message
import time
import random
import aiohttp
from userbot import UserBot
from userbot.plugins.help import add_command_help

MEME_API_URL = "https://meme-api.com/gimme"
SUBREDDITS = ["memes", "dankmemes", "ProgrammerHumor", "me_irl", "MemeEconomy"]
COOLDOWN = 10  # seconds
cooldowns = {}

@UserBot.on_message(filters=filters.me & filters.command(["meme"], "."))
async def meme_command(client: UserBot, message: Message):
    # Cooldown check
    user_id = message.from_user.id
    now = time.time()
    if now - cooldowns.get(user_id, 0) < COOLDOWN:
        remaining = int(COOLDOWN - (now - cooldowns.get(user_id, 0)))
        await message.edit(f"⏳ Cooldown: {remaining}s")
        return
    cooldowns[user_id] = now

    try:
        # Create local session for this request
        async with aiohttp.ClientSession() as session:
            subreddit = random.choice(SUBREDDITS)
            async with session.get(f"{MEME_API_URL}/{subreddit}") as resp:
                if resp.status != 200:
                    await message.edit("🔧 Meme API timeout!")
                    return

                data = await resp.json()
                if data.get("nsfw", False):
                    await message.edit("🚫 NSFW blocked!")
                    return

                # Build and send response
                await message.delete()
                await client.send_photo(
                    message.chat.id,
                    data['url'],
                    caption=(
                        f"**{data['title']}**\n\n"
                        f"⬆️ {data.get('ups', 0)} | "
                        f"📌 r/{data.get('subreddit', 'memes')}\n"
                        f"`{data['url']}`"
                    )
                )

    except aiohttp.ClientError:
        await message.edit("🌐 Connection failed!")
    except Exception as e:
        await message.edit("❌ Meme machine broke!")
        print(f"Meme error: {str(e)}")