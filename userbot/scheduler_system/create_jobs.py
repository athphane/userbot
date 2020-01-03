import userbot
from userbot import scheduler


def set_client(new_client):
    userbot.client = new_client


def add_job(function):
    scheduler.add_job(function, 'interval', seconds=3, args=[userbot.client])
