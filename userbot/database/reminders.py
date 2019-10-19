from userbot.database import database
from userbot.helpers.utility import get_random_hex

self_reminders = database['self_reminders']


class Reminders:
    @staticmethod
    def get_all_reminders():
        query = self_reminders.find({}, {"_id": 0})
        reminders = []

        for item in query:
            reminder_element = [item['unique_id'], item['content']]
            reminders.append(reminder_element)

        return reminders

    @staticmethod
    def add_reminder(content):
        query = {
            'unique_id': str(get_random_hex()),
            'content': str(content)
        }

        self_reminders.insert_one(query)

    @staticmethod
    def find_reminder(unique_id):
        query = {
            "unique_id": str(unique_id),
        }

        return self_reminders.find_one(query)

    @staticmethod
    def delete_reminder(unique_id):
        query = {
            'unique_id': unique_id,
        }

        self_reminders.delete_one(query)
