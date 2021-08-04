from pyrogram.types import Message

from userbot.database import database


class StickerDeleter:
    def __init__(self):
        self.sticker_table = database()["sticker_deleter"]

    def get_chat_ids(self):
        return self.sticker_table.find({}, {"chat_id": 1, "_id": 0})

    def add_sticker_in_chat(self, message: Message):
        data = {
            "chat_id": message.chat.id,
            "sticker_id": message.sticker.file_unique_id,
        }

        self.sticker_table.insert_one(data)

    def find_chat_id(self, message: Message):
        data = {
            "chat_id": message.chat.id,
            "sticker_id": message.sticker.file_unique_id,
        }

        return self.sticker_table.find_one(data)

    def delete_sticker_in_chat(self, message: Message):
        data = {
            "chat_id": message.chat.id,
        }

        exists = self.sticker_table.find_one(data)

        if exists is None:
            return False
        else:
            query = {
                "chat_id": message.chat.id,
            }
            self.sticker_table.delete_many(query)
            return True

