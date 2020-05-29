import ast
import logging
from configparser import ConfigParser
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from userbot.userbot import UserBot

# Logging at the start to catch everything
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    handlers=[
        TimedRotatingFileHandler('logs/userbot.log', when="midnight", encoding=None,
                                 delay=False, backupCount=10),
        logging.StreamHandler()
    ]
)
LOGS = logging.getLogger(__name__)

# Read from config file
name = UserBot().__class__.__name__.lower()
config_file = f"{name}.ini"
config = ConfigParser()
config.read(config_file)

# MongoDB details
MONGO_URL = config.get('mongo', 'url')
DB_NAME = config.get('mongo', 'db_name')
DB_USERNAME = config.get('mongo', 'db_username')
DB_PASSWORD = config.get('mongo', 'db_password')

# Other Users
ALLOWED_USERS = ast.literal_eval(config.get('users', 'allowed_users', fallback='[]'))

# MISC APIs
YOURLS_URL = config.get('misc', 'yourls_url', fallback=None)
YOURLS_KEY = config.get('misc', 'yourls_key', fallback=None)
YANDEX_API_KEY = config.get('yandex', 'key', fallback=None)

# Extra details
__version__ = '0.2.0'
__author__ = 'athphane'

# Get the Values from our .env
PM_PERMIT = config.get('pm_permit', 'pm_permit')
PM_LIMIT = int(config.get('pm_permit', 'pm_limit'))

LOG_GROUP = config.get('logs', 'log_group')

# Scheduler
scheduler = AsyncIOScheduler()

# Global Variables
CMD_HELP = {}
client = None
START_TIME = datetime.now()
