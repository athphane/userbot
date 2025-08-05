
from userbot.database import database
from datetime import datetime

class Ignore:
    def __init__(self):
        self.ignore_table = database()["ignored_users"]

    def ignore_user(self, user_id):
        self.ignore_table.insert_one({"user_id": user_id, "ignored": True, "last_message_time": None})

    def unignore_user(self, user_id):
        self.ignore_table.delete_one({"user_id": user_id})

    def is_ignored(self, user_id):
        return self.ignore_table.find_one({"user_id": user_id, "ignored": True}) is not None

    def set_last_message_time(self, user_id):
        self.ignore_table.update_one({"user_id": user_id}, {"$set": {"last_message_time": datetime.now()}})

    def get_last_message_time(self, user_id):
        user = self.ignore_table.find_one({"user_id": user_id})
        if user:
            return user.get("last_message_time")
        return None

ignore_db = Ignore()
