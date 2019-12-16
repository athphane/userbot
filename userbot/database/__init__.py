import pymongo
from userbot import MONGO_URL, DB_USERNAME, DB_PASSWORD, DB_NAME


def database():
    """Created Database connection"""
    client = pymongo.MongoClient(
        MONGO_URL,
        username=DB_USERNAME,
        password=DB_PASSWORD
    )
    db = client[DB_NAME]
    return db

