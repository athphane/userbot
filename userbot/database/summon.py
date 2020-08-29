from pymongo import ReturnDocument
from pyrogram.types import Message

from userbot.database import database


class SUMMON:
    def __init__(self):
        self.summon_table = database()['summon']

    def get_chat_ids(self):
        return self.summon_table.find({}, {"chat_id": 1, '_id': 0})

    def add_chat_id(self, message: Message):
        data = {
            'chat_id': message.chat.id,
        }

        self.summon_table.insert_one(data)

    def update(self, message: Message, last_send, next_send):
        query = {
            'chat_id': message.chat.id,
        }

        update = {
            "$set": {
                "last_send": last_send,
                "next_send": next_send
            }
        }

        self.summon_table.find_one_and_update(query, update, return_document=ReturnDocument.AFTER)

    def find_chat_id(self, message: Message):
        query = {
            'chat_id': message.chat.id,
        }

        return self.summon_table.find_one(query)

    def delete_chat_id(self, message: Message):
        exists = self.find_chat_id(message)

        if exists is None:
            return False
        else:
            query = {
                'chat_id': message.chat.id,
            }
            self.summon_table.delete_one(query)
            return True
