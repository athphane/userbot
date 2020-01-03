from userbot.userbot import UserBot
from userbot import scheduler
import userbot

if __name__ == '__main__':
    app = UserBot()

    userbot.client = app

    scheduler.start()

    app.run()
