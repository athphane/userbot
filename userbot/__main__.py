from userbot import BOT, __version__, LOGS

BOT.start()
ME = BOT.get_me().username
LOGS.info(f"You're logged in as \"{ME}\"! Test it by typing .alive in any chat.")
LOGS.info(f"Your bot is Version {__version__}\n")
BOT.idle()
