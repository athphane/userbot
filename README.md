# B LAC TEÀM USERBOT
![Python Version](https://img.shields.io/badge/Python-v3.8-blue)
![Repo Size](https://img.shields.io/github/repo-size/athphane/userbot)
[![Commit Activity](https://img.shields.io/github/commit-activity/w/athphane/userbot)](https://github.com/athphane/userbot/pulse)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b10d40c60fc549299eeb7bda1c7501aa)](https://app.codacy.com/manual/athphane/userbot?utm_source=github.com&utm_medium=referral&utm_content=athphane/userbot&utm_campaign=Badge_Grade_Settings)
[![HitCount](http://hits.dwyl.com/athphane/userbot.svg)](http://hits.dwyl.com/athphane/userbot)
[![Contributors](https://img.shields.io/github/contributors/athphane/userbot)](https://github.com/athphane/userbot/graphs/contributors)
![Last Commit](https://img.shields.io/github/last-commit/athphane/userbot/master)
![Issues](https://img.shields.io/github/issues/athphane/userbot)
![Pull Requests](https://img.shields.io/github/issues-pr/athphane/userbot)
[![StyleCI](https://github.styleci.io/repos/216083990/shield?branch=master)](https://github.styleci.io/repos/216083990)
[![License](https://img.shields.io/github/license/athphane/userbot)](LICENSE)

<img src="https://i.imgur.com/WXUgDHT.png" width="160" align="right">

> A Telegram Userbot based on [B LAC ](https://github.com/pyrogram/pyrogram)

This repository contains the source code of a Telegram Userbot and the instructions for running a
copy yourself. Beside its main purpose, the bot is featuring [**Pyrogram Asyncio**](https:////github.com/pyrogram/pyrogram/issues/181) and
[**Smart Plugins**](https://docs.pyrogram.org/topics/smart-plugins); feel free to explore the source code to
learn more about these topics.

I assume you will read this whole README.md file before continuing.

> Development in progress.

## Requirements
You're gonna need to get the following programs and services either installed on your server
or signed up for. You must do all. It is a cardinal sin if you don't.

* `virtualenv` installed so that the packages don't interfere with other system packages.

* [MongoDB](https://www.mongodb.com) on your server or a free server from 
[MongoDB Atlas](https://www.mongodb.com/cloud/atlas). (I recommend Atlas as I used it during
development with no issues.)

* [carbon-now-cli](https://github.com/mixn/carbon-now-cli) on your server too generate code images for the
[carbon.py](/userbot/plugins/carbon.py) module. I use this CLI tool cause I don't know and couldn't get selenium
and chromedriver to work nicely on my server/code. I'll be nice and even give you the command to install this.
I assume you already have NPM installed. 
    ```
    Windows: npm install -g carbon-now-cli
    Linux: sudo npm install -g carbon-now-cli --unsafe-perm=true --allow-root
    MacOS: I assume almost the same as linux ¯\_(ツ)_/¯
    ``` 

## Installing
*One Click Deploy*
Quick Deploy on Heroku using the button down below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/athphane/userbot)

*The way I deploy*
```bash
git clone https://github.com/athphane/userbot.git
cd userbot
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python -m userbot.
```

## Developing
To add extra modules to the bot, simply add the code into [userbot/plugins](userbot/plugins). Each file
that is added to the plugins directory should have the following code at a minimum.
```python
from pyrogram import Message, Filters

from userbot import UserBot

@UserBot.on_message(Filters.command('sample', ['.']))
async def module_name(bot: UserBot, message: Message):
    await message.edit(
        "This is a sample module"
    )
```

This example is only for Pyrogram on_message events. 

## Credits, and Thanks to
*  [Dan](https://t.me/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)

*  [Colin Shark](https://t.me/ColinShark) for his [PyroBot](https://git.colinshark.de/PyroBot/PyroBot) which helped with
most of the useful functions used.

*  The people at [MyPaperPlane](https://github.com/MyPaperPlane) for their [Telegram-UserBot](https://github.com/MyPaperPlane/Telegram-UserBot)
that gave a ton of ideas on how and what modules to include in this userbot. 

*  [Baivaru](https://github.com/baivaru) for the ton of help that got me this far into making this repo. 

---
<pBuild Status Python Version Release Stars Forks Issues Open Issues Closed PRs Open PRs Closed Contributors Repo Size License Commit Activity Plugins Repo! Join Channel! DeepSource Gitpod ready-to-code

Userge is a Powerful , Pluggable Telegram UserBot written in Python using Pyrogram.

Documentation 📘
you can find full documentation here

Inspiration 😇
This project is inspired by the following projects :)

tg_userbot ( heavily ) 🤗
PyroGramBot
Telegram-Paperplane
UniBorg
Special Thanks to all of you !!!.

How To Deploy 👷
With Heroku 🇭
Deploy

With Docker 🐳

With Git, Python and pip 🔧

Video Tutorial 🎥
Tutorial

Support & Discussions 👥
Head over to the Discussion Group and Update Channel

Project Credits 💆‍♂️
Specially to these projects 🥰
Contributors 👥
Copyright & License 👮
Copyright (C) 2020 by UsergeTeam ❤️️
Licensed under the terms of the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
