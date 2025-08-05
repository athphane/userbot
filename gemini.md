This is a Telegram Userbot built with Python and the Pyrogram library. It uses a MongoDB database for data storage and offers a variety of features through a plugin-based architecture.

**Key Technologies:**

*   **Programming Language:** Python 3.10
*   **Telegram Library:** Pyrogram
*   **Database:** MongoDB
*   **Dependency Management:** pip and `requirements.txt`
*   **Deployment:** Can be run directly or with Docker.

**Project Structure:**

*   `userbot/`: Main application directory.
    *   `userbot.py`: Core `UserBot` client class.
    *   `__main__.py`: Application entry point.
    *   `plugins/`: Contains the bot's command plugins.
    *   `database/`: Manages the MongoDB database connection and collections.
*   `requirements.txt`: Lists all Python dependencies.
*   `config/userbot.ini.sample`: Sample configuration file.
*   `docker-compose.yml`: For Docker-based deployment.
*   `README.md`: Detailed setup and usage instructions.

**Features:**

The bot provides a wide range of features through its plugins, including:

*   **Core:** AFK status, help, metrics, restart, and update functionality.
*   **Tools:** Carbon code image generation, dictionary, translation, Urban Dictionary, weather, and more.
*   **Fun:** Memes, pats, text replacement, and other entertainment commands.
*   **Music:** Spotify integration and lyrics fetching.
*   **Admin:** Administrative commands for managing the bot.

**Setup and Configuration:**

1.  **Prerequisites:** Python 3.10, `virtualenv`, MongoDB, and `carbon-now-cli`.
2.  **Installation:**
    *   Clone the repository.
    *   Create and activate a virtual environment.
    *   Install dependencies from `requirements.txt`.
3.  **Configuration:**
    *   Copy `userbot.ini.sample` to `userbot.ini`.
    *   Fill in the required API keys and settings (Telegram API, MongoDB connection string, etc.).
4.  **Running the Bot:**
    *   Run `python -m userbot` to start the bot.
    *   Alternatively, use the provided `docker-compose.yml` for a Docker-based setup.

**Spotify Integration:**

To enable Spotify features, you need to:

1.  Create a Spotify Developer application.
2.  Set the Redirect URI to `http://localhost:8888/callback`.
3.  Add your `CLIENT_ID` and `CLIENT_SECRET` to `userbot.ini`.
4.  Run `python spotify.py` to generate a `.cache` file, which needs to be in the project root.

**Database:**

The bot uses MongoDB for various features, including:

*   Auto-replies
*   PM permit
*   User profiles
*   Reminders
*   Settings
*   Sticker deleter
*   Summon