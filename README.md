# Kurigram Userbot
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![Repo Size](https://img.shields.io/github/repo-size/athphane/userbot)
[![Commit Activity](https://img.shields.io/github/commit-activity/w/athphane/userbot)](https://github.com/athphane/userbot/pulse)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b10d40c60fc549299eeb7bda1c7501aa)](https://app.codacy.com/manual/athphane/userbot?utm_source=github.com&utm_medium=referral&utm_content=athphane/userbot&utm_campaign=Badge_Grade_Settings)
[![HitCount](http://hits.dwyl.com/athphane/userbot.svg)](http://hits.dwyl.com/athphane/userbot)
[![Contributors](https://img.shields.io/github/contributors/athphane/userbot)](https://github.com/athphane/userbot/graphs/contributors)
![Last Commit](https://img.shields.io/github/last-commit/athphane/userbot/master)
![Issues](https://img.shields.io/github/issues/athphane/userbot)
![Pull Requests](https://img.shields.io/github/issues-pr/athphane/userbot)
[![License](https://img.shields.io/github/license/athphane/userbot)](LICENSE)

<img src="https://i.imgur.com/WXUgDHT.png" width="160" align="right">

> A Telegram Userbot based on [Kurigram](https://github.com/KurimuzonAkuma/kurigram)

This repository contains the source code of a Telegram Userbot and the instructions for running a
copy yourself. The bot uses Kurigram's asynchronous client and
[**Smart Plugins**](https://docs.kurigram.icu/topics/smart-plugins); feel free to explore the source code to
learn more about these topics.

Kurigram keeps the `pyrogram` import namespace. Existing `[pyrogram]` configuration
and session files continue to use the same names. Native encryption is provided
by `TgCrypto-pyrofork`, as in KinTab.

I assume you will read this whole README.md file before continuing.

## Requirements
You're gonna need to get the following programs and services either installed on your server
or signed up for. You must do all. It is a cardinal sin if you don't.
* Python 3.10 or newer. Version-specific dependency pins select the newest compatible
  releases for Python 3.10, 3.11, and 3.12+. The Docker images use Python 3.15.
* `virtualenv` installed so that the packages don't interfere with other system packages.
* A C compiler, Python headers, Cairo development headers, and `pkg-config` for
  SVG-to-PNG rendering. On Debian/Ubuntu, install them with
  `sudo apt-get install build-essential python3-dev libcairo2-dev pkg-config`.
  The Docker images include these dependencies.
* [Deno](https://docs.deno.com/runtime/getting_started/installation/) 2.3+ on `PATH`
  for YouTube downloads, plus FFmpeg for merging video and audio. Both are included
  in the Docker images. The `yt-dlp[default]` requirement supplies the matching
  [YouTube challenge scripts](https://github.com/yt-dlp/yt-dlp/wiki/EJS).
  HTTP 429 means the service is rate-limiting requests; wait before retrying and
  check the server/proxy's public IP if it persists. Installing Deno does not
  remove a rate limit.

* Storage uses SQLite, included with Python. The database is created automatically
  at `config/userbot.sqlite3`.

## Installation and Deployment
*The way I deploy*
```bash
git clone https://github.com/athphane/userbot.git
cd userbot
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python -m userbot
```
When upgrading an existing virtual environment from pyrotgfork, remove the old
packages before reinstalling so their shared modules are replaced completely:
```bash
python -m pip uninstall -y pyrotgfork TgCrypto
python -m pip install --upgrade --force-reinstall -r requirements.txt
```
Docker deployments install the new dependencies in a fresh image.

*Using docker*
- Save the following content as `docker-compose.yml`
```yml
services:
  userbot:
    hostname: userbot
    volumes:
      - ./config:/root/userbot/config
    image: ghcr.io/athphane/userbot:latest
    restart: always
    labels:
      com.centurylinklabs.watchtower.enable: "true"
```
If you already run Watchtower on this Docker host, these labels opt the userbot
into automatic updates from `ghcr.io/athphane/userbot:latest`.
Watchtower must be configured to include this container and allow updates; the
userbot is also opted in when Watchtower uses `--label-enable`. See the
[Watchtower container selection documentation](https://containrrr.dev/watchtower/container-selection/)
for name and scope filters. After adding the labels to an existing deployment,
run `docker compose up -d userbot` to apply them.

This example uses the published image. The repository's root `docker-compose.yml`
builds locally and mounts the source checkout, so its labels alone do not enable
updates from the published image.

- Config \
 Get your telegram api_id and api_hash from [https://my.telegram.org/apps](https://my.telegram.org/apps) and configure them:
```
mkdir config
wget -O config/userbot.ini https://raw.githubusercontent.com/athphane/userbot/refs/heads/master/userbot.ini.sample
nano config/userbot.ini
```
- First run:
```bash
docker compose run --rm userbot python -m userbot
```
- Configure userbot and stop container **CTRL+C**
- Run the container again de-attached:
```bash
docker compose up -d
```
## Local database

PM approvals, ignored users, reminders, profiles, summon settings, sticker rules,
and auto-replies are stored in `config/userbot.sqlite3`. Python's built-in
`sqlite3` module handles storage, with no additional package or service.
The existing `database()["collection"]` and helper APIs remain available.
ID lookups are indexed; the adapter supports equality filters, string
`$regex` searches with `$options`, projections, `$set`, `$inc`, `$unset`,
and upserts. It is a small adapter for the bot's calls, not a full MongoDB driver;
unsupported operators raise errors. Music, lyrics, and Telegram message searches
continue to query their existing external services.

The optional configuration below changes the file location. Relative paths are
resolved from the working directory used to run the bot. Docker's existing
`./config:/root/userbot/config` mount persists the default file.

```ini
[database]
path = config/userbot.sqlite3
```

Existing configuration files work without this section; old `[mongo]` settings
are ignored. A new SQLite file starts empty. Existing MongoDB records are **not
copied automatically**. To preserve them before switching:

1. Stop the bot so records cannot change during export and import.
2. Export each collection with MongoDB Database Tools. Set `MONGODB_URI` to
   your existing connection URI and replace `userbot` if your database name differs:

   ```bash
   mkdir -p exports
   for collection in auto_replies ignored_users pmpermit profiles self_reminders settings sticker_deleter summon; do
     mongoexport --uri="$MONGODB_URI" --db=userbot --collection="$collection" --jsonArray --out="exports/$collection.json"
   done
   ```

3. Import on the host from the repository root:

   ```bash
   python userbot/database/migrate.py exports --database config/userbot.sqlite3
   ```

   For a published Docker image, mount the export directory for this one command:

   ```bash
   docker compose run --rm -v "$PWD/exports:/exports:ro" userbot python userbot/database/migrate.py /exports --database config/userbot.sqlite3
   ```

   The importer accepts JSON arrays or newline-delimited JSON and preserves
   ObjectId values as strings, dates as Python datetimes, and numeric values.
   It requires only Python's standard library and refuses to merge into
   nonempty destination collections. All files import in one transaction; a
   failed import leaves existing records unchanged.
4. Start the bot and check your reminders and settings. Once verified, remove
   the old MongoDB service from your deployment. Keep its data and exports
   until you have verified the migration.

To back up SQLite, stop the bot and copy the database file, or use SQLite's
`Connection.backup()` API for a running bot. SQLite may create `-wal` and
`-shm` files while running, so copying only the main file while it is open
is not a complete backup. Use a local filesystem for the database.

## Social media downloads

Your own TikTok, Instagram, and YouTube Shorts links download automatically in
any chat. The owner `.dl` reply command also works in any chat. Links from other
people are ignored until you send `.socialdl on` in that chat or group. Send
`.socialdl off` there to disable them, `.socialdl status` to check the current
chat, or `.socialdl list` to see enabled chat IDs. In enabled groups, TikTok,
Instagram, and YouTube Shorts links download automatically; in enabled private
chats, supported links download automatically. Only your account can use the
`.socialdl` and `.dl` commands; incoming `/start`, `/help`, and `/dl` commands
are ignored.

Chat settings are stored in `config/social_dl_chats.json` and survive restarts.
The old `enabled`, `allowed_group`, `ignored_users`, and private user allowlist
settings no longer affect downloads. FFmpeg and ffprobe are needed to make
YouTube uploads streamable and to render Instagram
photos with music. Instagram photo-only carousels (up to 20 images) are sent
in order as albums of up to 10 photos, with one caption per post. Mixed
photo/video carousels are not supported by the photo fallback. Media larger than 50 MB is rejected for chat downloads.

## Spotify integration

To get the Spotify commands working on the Userbot, you need to get a CLIENT_ID and CLIENT_SECRET
form the [Spotify Developer Portal](https://developer.spotify.com/dashboard/applications) and add
them into your userbot.ini file.

On the Spotify developer portal, make sure to set your application `Redirect URI` to 
'http://localhost:8888/callback'. 

Now is a good time 
Then go ahead and run the command `python spotify.py` 
in the projects root directory. 

This will create a file called `.cache-yourusername`. You need to transfer this file to the
project root of the server that will be running your userbot. This is a one time setup.


## Known issues
* `.restart` command do not work on Termux as [psutils is not supported on Android](https://github.com/giampaolo/psutil/issues/913). \
CTRL+C, run `git pull` and `python -m userbot` to update bot on termux.

## Star History

<a href="https://star-history.com/#athphane/userbot&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=athphane/userbot&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=athphane/userbot&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=athphane/userbot&type=Date" />
  </picture>
</a>


## Credits, and Thanks to
*  [Dan](https://t.me/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
*  [Colin Shark](https://t.me/ColinShark) for his [PyroBot](https://git.colinshark.de/PyroBot/PyroBot) which helped with
most of the useful functions used.
*  The people at [MyPaperPlane](https://github.com/MyPaperPlane) for their [Telegram-UserBot](https://github.com/MyPaperPlane/Telegram-UserBot)
that gave a ton of ideas on how and what modules to include in this userbot.
*  [Baivaru](https://github.com/baivaru) for the ton of help that got me this far into making this repo.
---
<p align="center">Made with love from the Maldives ❤</p>
