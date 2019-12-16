from pyrogram import Client
from configparser import ConfigParser


class UserBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        config_file = f"{name}.ini"

        config = ConfigParser()
        config.read(config_file)

        super().__init__(
            name,
            config_file=config_file,
            workers=16,
            plugins=dict(root="userbot/plugins"),
            workdir="./",
            app_version=f"Userbot v0.2",
            device_model="Python",
            system_version="v0.2"
        )

    async def start(self):
        await super().start()
        print(f"Userbot started. Hi.")

    async def stop(self):
        await super().stop()
        print("Userbot stopped. Bye.")
