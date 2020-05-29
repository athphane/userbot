import userbot
from userbot import scheduler
from userbot.userbot import UserBot

if __name__ == '__main__':
    app = UserBot()

    userbot.client = app

    scheduler.start()

    app.run()
