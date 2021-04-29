import os
import sys
from configparser import ConfigParser

import psutil
from pyrogram import Client
from pyrogram.raw.all import layer


class UserBot(Client):
    def __init__(self, version='0.0.0'):
        self.version = version
        self.name = name = self.__class__.__name__.lower()
        config_file = f"{name}.ini"

        self.config = ConfigParser().read(config_file)

        super().__init__(
            name,
            config_file=config_file,
            plugins=dict(root=f"{name}/plugins"),
            workdir="./",
            app_version=self.version
        )

    async def start(self):
        await super().start()

        restart_reply_details = super().search_messages("me", query="#userbot_restart")
        async for x in restart_reply_details:
            _, chat_id, message_id = x.text.split(", ")

            await super().edit_message_text(
                int(chat_id), int(message_id), "`Userbot Restarted!`"
            )

            await super().delete_messages("me", x.message_id)

            break

        me = await self.get_me()

        print(f"{self.__class__.__name__} v{self.version} (Layer {layer}) started on @{me.username}.\n"
              f"Hi!")

    async def stop(self, *args):
        await super().stop()
        print(f"{self.__class__.__name__} v{self.version} Stopped. Bye.")

    async def restart(self, *args, git_update=False, pip=False):
        await self.stop()

        try:
            c_p = psutil.Process(os.getpid())
            for handler in c_p.open_files() + c_p.connections():
                os.close(handler.fd)
        except Exception as c_e:
            print(c_e)

        if git_update:
            os.system("git reset --hard")
            os.system("git pull")
        if pip:
            os.system("pip install -U -r requirements.txt")

        os.execl(sys.executable, sys.executable, "-m", self.__class__.__name__.lower())
        sys.exit()
