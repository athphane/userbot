from pyrogram.types import Message

from userbot.database import database


class AutoReplies:
    def __init__(self):
        self.auto_replies_table = database()["auto_replies"]

    def get_chat_ids(self):
        return self.auto_replies_table.find({}, {"chat_id": 1, "_id": 0})

    def add_auto_reply_in_char(self, message: Message):
        data = {
            "chat_id": message.chat.id,
            "user_id": message.from_user.id,

        }

        self.auto_replies_table.insert_one(data)

    def add_sticker_in_chat(self, message: Message):
        data = {
            "chat_id": message.chat.id,
            "sticker_id": message.sticker.file_unique_id,
        }

        self.auto_replies_table.insert_one(data)

    def find_chat_id(self, message: Message):
        data = {
            "chat_id": message.chat.id,
            "sticker_id": message.sticker.file_unique_id,
        }

        return self.auto_replies_table.find_one(data)

    def delete_sticker_in_chat(self, message: Message):
        data = {
            "chat_id": message.chat.id,
        }

        exists = self.auto_replies_table.find_one(data)

        if exists is None:
            return False
        else:
            query = {
                "chat_id": message.chat.id,
            }
            self.auto_replies_table.delete_many(query)
            return True

