import pymongo
import os

MONGOURL = os.environ.get("MONGO_URL")
mongo_database_name = os.environ.get("MONGO_DB_NAME")

"""Create Database connection"""
client = pymongo.MongoClient(
    MONGOURL,
)

"""Database Instance"""
database = client[mongo_database_name]

