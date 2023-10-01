import ast
import logging
import os
from configparser import ConfigParser
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from userbot.userbot import UserBot

# Created logs folder if it is not there. Needed for logging.
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create config folder if it is not there. Needed for config.
if not os.path.exists('config'):
    os.makedirs('config')

# Move the userbot.ini file from root to config folder if it is not there.
if not os.path.exists('config/userbot.ini'):
    os.rename('userbot.ini', 'config/userbot.ini')

# Move the userbot.session file from root to config folder if it is not there.
if not os.path.exists('config/userbot.session'):
    os.rename('userbot.session', 'config/userbot.session')


# Logging at the start to catch everything
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    handlers=[
        TimedRotatingFileHandler(
            "logs/userbot.log",
            when="midnight",
            encoding=None,
            delay=False,
            backupCount=10,
        ),
        logging.StreamHandler(),
    ],
)
LOGS = logging.getLogger(__name__)

# Extra details
__version__ = "0.2.0"
__author__ = "athphane"

UserBot = UserBot(__version__)

# Read from config file
config_file = 'config/userbot.ini'
config = ConfigParser()
config.read(config_file)

# MongoDB details
MONGO_URL = config.get("mongo", "url")
DB_NAME = config.get("mongo", "db_name", fallback="userbot")
DB_USERNAME = config.get("mongo", "db_username")
DB_PASSWORD = config.get("mongo", "db_password")
IS_ATLAS = config.getboolean("mongo", "is_atlas", fallback=False)

# Other Users
ALLOWED_USERS = ast.literal_eval(
    config.get("users", "allowed_users", fallback="[]")
)

# MISC APIs
YOURLS_URL = config.get("misc", "yourls_url", fallback=None)
YOURLS_KEY = config.get("misc", "yourls_key", fallback=None)
YANDEX_API_KEY = config.get("yandex", "key", fallback=None)
SPOTIFY_USERNAME = config.get("spotify", "username", fallback=None)
SPOTIFY_CLIENT_ID = config.get("spotify", "client_id", fallback=None)
SPOTIFY_CLIENT_SECRET = config.get(
    "spotify", "client_secret", fallback=None)

# Get the Values from our .env
PM_PERMIT = config.get("pm_permit", "pm_permit")
PM_LIMIT = int(config.get("pm_permit", "pm_limit"))
LOG_GROUP = config.get("logs", "log_group")

# Scheduler
scheduler = AsyncIOScheduler()

# Global Variables
CMD_HELP = {}
client = None
START_TIME = datetime.now()
