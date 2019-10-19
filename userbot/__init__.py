from pyrogram import Client
import logging
import os
import dotenv
import sys

# We need logging so early
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARN)
LOGS = logging.getLogger(__name__)

# Check for Python 3.6 or newer
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGS.error("You MUST use at least Python 3.6. Bot Quitting")
    quit(1)

# some details
__version__ = '0.2.0'
__author__ = 'athphane'

# Load env variables from file
dotenv.load_dotenv()

# Get the Values from our .env
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

# Create the client
BOT = Client(
    'userbot',
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="userbot/plugins"),
    app_version=f"Userbot \U0001f525 v{__version__}",
    device_model="Python",
    system_version=str(__version__),
    workers=20,
)

# Global Variables
CMD_HELP = {}
