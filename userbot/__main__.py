import asyncio

from pyrogram import idle


async def main() -> None:
    """Run the client and scheduler on one loop and stop both on shutdown."""
    import userbot
    from userbot import UserBot, scheduler

    userbot.client = UserBot
    started = False
    try:
        await UserBot.start()
        started = True
        scheduler.start()
        await idle()
    finally:
        if scheduler.running:
            scheduler.shutdown()
            await asyncio.sleep(0)
        if started:
            await UserBot.stop()


if __name__ == "__main__":
    asyncio.run(main())
