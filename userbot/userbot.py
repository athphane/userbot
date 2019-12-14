from pyrogram import Client
from configparser import ConfigParser
from userbot import __version__


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
            app_version=f"Userbot \U0001f525 v{__version__}",
            device_model="Python",
            system_version=str(__version__)
        )

    async def start(self):
        await super().start()
        print(f"Userbot started. Hi.")

    async def stop(self):
        await super().stop()
        print("Userbot stopped. Bye.")
