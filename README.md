# Pyrogram Userbot

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b10d40c60fc549299eeb7bda1c7501aa)](https://app.codacy.com/manual/athphane/userbot?utm_source=github.com&utm_medium=referral&utm_content=athphane/userbot&utm_campaign=Badge_Grade_Settings)

A Telegram Userbot based on [Pyrogram](https://github.com/pyrogram/pyrogram)

I assume you will read this whole README.md file before continuing.

Development in progress.

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

There is no one click deploy.. It was all a ruse. You have to deploy like how I deploy it...

*The way I deploy*
```bash
git clone https://github.com/athphane/userbot.git
cd userbot
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python -m userbot.
```


### Some more setup needed

* Open file_ids.txt, remove EVERYTHING in that file and only put in ```{}```. That's it.
That file is used for the [picture.py](/userbot/plugins/memes/fixed_memes.py) module so that it can send the
images a second time much faster rather than to upload them again. In a later life I will make
this file create itself.


## Credits, and Thanks to
* [Dan](https://t.me/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
* [Colin Shark](https://t.me/ColinShark) for his [PyroBot](https://git.colinshark.de/PyroBot/PyroBot) which helped with
most of the useful functions used.
* The people at [MyPaperPlane](https://github.com/MyPaperPlane) for their [Telegram-UserBot](https://github.com/MyPaperPlane/Telegram-UserBot)
that gave a ton of ideas on how and what modules to include in this userbot. 
* [Baivaru](https://github.com/baivaru) for the ton of help that got me this far into making this repo. 

---
Made with love from the Maldives <3