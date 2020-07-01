import userbot
from userbot import UserBot
from userbot import scheduler

if __name__ == '__main__':
    userbot.client = UserBot

    scheduler.start()

    UserBot.run()
