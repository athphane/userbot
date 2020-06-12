import os
import sys
from configparser import ConfigParser

import psutil
from pyrogram import Client


class UserBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        config_file = f"{name}.ini"

        config = ConfigParser()
        config.read(config_file)

        super().__init__(
            name,
            config_file=config_file,
            workers=32,
            plugins=dict(root="userbot/plugins"),
            workdir="./",
            app_version=f"Userbot v0.2",
            device_model="Python",
            system_version="v0.2"
        )

    async def start(self):
        await super().start()

        restart_reply_details = super().search_messages('me', query='#userbot_restart')
        async for x in restart_reply_details:
            _, chat_id, message_id = x.text.split(', ')
            await super().edit_message_text(int(chat_id), int(message_id), "`Userbot Restarted!`")
            await super().delete_messages('me', x.message_id)
            break

        print(f"Userbot started. Hi.")

    async def stop(self, *args):
        await super().stop()
        print("Userbot stopped. Bye.")

    async def restart(self, git_update=False, pip=False, *args):
        """ Shoutout to the Userg team for this."""
        await self.stop()
        try:
            c_p = psutil.Process(os.getpid())
            for handler in c_p.open_files() + c_p.connections():
                os.close(handler.fd)
        except Exception as c_e:
            print(c_e)

        if git_update:
            os.system('git reset --hard')
            os.system('git pull')
        if pip:
            os.system('pip install -U -r requirements.txt')

        os.execl(sys.executable, sys.executable, '-m', self.__class__.__name__.lower())
        sys.exit()
