# Pyrogram Userbot
A Telegram Userbot based on [Pyrogram](https://github.com/pyrogram/pyrogram)

Development in progress.


## Requirements
You're gonna need to get the following programs and services either installed on your server
or signed up for.

* `virtualenv` installed so that the packages don't interfere with other system packages.
* [MongoDB]("https://www.mongodb.com") on your server or a free server from 
[MongoDB Atlas]("https://www.mongodb.com/cloud/atlas"). (I recommend Atlast as I used it during
development with no issues.)

## Installing
*One Click Deploy*

There is no one click deploy.. It was all a ruse. You have to deploy like how I deploy it...

*The way I deploy*
```bash
git https://github.com/athphane/userbot.git
cd userbot
virtualenv venv
source venv/bin/acticate
pip install -r requirements.txt
python -m userbot.
```

## Credits, and Thanks to
* [Dan Tès](https://t.me/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
* [Colin Shark](https://t.me/ColinShark) for his [PyroBot](https://git.colinshark.de/PyroBot/PyroBot) which helped with
most of the useful functions used.
* [Baivaru](https://github.com/baivaru) for the ton of help that got me this far into making this repo. 
