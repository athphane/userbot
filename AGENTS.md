# AGENTS.md

This file contains guidelines for agentic coding agents working on this repository.

## Build / Run / Test Commands

- **Run the userbot:** `python -m userbot`
- **Run with docker:** `docker compose up -d`
- **First time setup (docker):** `docker compose run --rm userbot python -m userbot`
- **Install dependencies:** `pip install -r requirements.txt`
- **Update pip requirements:** `pip install -U -r requirements.txt`

**Testing:** Run offline dependency compatibility checks with `python -m unittest discover -s tests -v`. Test Telegram features manually by running the bot.

**Linting/Formatting:** Use black, autopep8, and isort for formatting. DeepSource is configured to auto-format.

## Code Style Guidelines

### Imports
Order: standard library → third-party → local imports. Group with blank lines between sections.
```python
import asyncio
from datetime import datetime
from typing import Optional

from pyrogram import filters
from pyrogram.types import Message

from userbot import ALLOWED_USERS, UserBot
from userbot.helpers import utility
```

### Naming Conventions
- Functions: `snake_case` (e.g., `now_playing`, `ReplyCheck`)
- Classes: `PascalCase` (e.g., `UserBot`, `First`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `CMD_HELP`, `ALLOWED_USERS`)
- Variables: `snake_case` (e.g., `current_track`, `file_id`)

### Type Hints
Use type hints for function parameters and return values:
```python
async def now_playing(bot: UserBot, message: Message) -> None:
    ...
```

### Pyrogram Plugin Pattern
All plugins follow this structure:
```python
from pyrogram import filters
from pyrogram.types import Message

from userbot import ALLOWED_USERS, UserBot
from userbot.plugins.help import add_command_help

@UserBot.on_message(filters.command(["cmd"], ".") & (filters.me | filters.user(ALLOWED_USERS)))
async def handler_name(bot: UserBot, message: Message):
    ...
    await message.edit("response")

# Command help section
add_command_help(
    "module_name",
    [
        [".cmd", "Description"],
    ],
)
```

### Message Handling
- Use `message.edit()` to edit command messages
- Use `message.reply_to_message` to access replied messages
- Use `ReplyCheck(message)` from `userbot.helpers.PyroHelpers` to determine reply ID
- Handle errors gracefully with try-except blocks
- For long output (>4096 chars), write to file and use `message.reply_document()`

### Error Handling
```python
try:
    result = await some_function()
except Exception as e:
    await message.edit(f"Error: {e}")
    return
```

### Async/Await
All command handlers are async. Use `await` for I/O operations and async library calls.

### Docstrings
Use docstrings for functions and classes:
```python
def split_list(input_list, n):
    """
    Takes a list and splits it into smaller lists of n elements each.
    :param input_list: list to split
    :param n: number of elements per sublist
    :return: list of lists
    """
    ...
```

### Project Structure
- Entry point: `userbot/__main__.py` (run via `python -m userbot`)
- Config: `config/userbot.ini`
- Plugins: `userbot/plugins/*.py`
- Helpers: `userbot/helpers/*.py`
- Database: `userbot/database/`

### Config Access
Access config values through the global `config` object in `userbot/__init__.py`:
```python
from userbot import ALLOWED_USERS, MONGO_URL, DB_NAME, SPOTIFY_CLIENT_ID
```

### Logging
Use the `LOGS` logger from `userbot/__init__.py`:
```python
from userbot import LOGS
LOGS.error("Something went wrong")
```

### Command Filters
- Basic command: `filters.command("cmd", ".")`
- Only me: `& filters.me`
- Allowed users: `& filters.user(ALLOWED_USERS)`
- Combined: `& (filters.me | filters.user(ALLOWED_USERS))`

### Database
MongoDB connection via `userbot.database`. Access the database instance:
```python
from userbot.database import database
```

### Notes
- Python 3.10+ required
- This is a Telegram userbot based on Pyrogram
- Commands are prefixed with `.` (e.g., `.alive`, `.help`)
- Each plugin must call `add_command_help()` at the end to register help
- Avoid committing secrets or `.cache-*` files
