import pymongo

from userbot import MONGO_URL, DB_USERNAME, DB_PASSWORD, DB_NAME, IS_ATLAS


def database():
    """Created Database connection"""
    if IS_ATLAS:
        client = pymongo.MongoClient(
            MONGO_URL,
        )
    else:
        client = pymongo.MongoClient(
            MONGO_URL,
            username=DB_USERNAME,
            password=DB_PASSWORD
        )
    db = client[DB_NAME]
    return db

