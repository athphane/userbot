from userbot.database import database
from userbot.helpers.utility import get_random_hex


class Reminders:
    def __init__(self):
        self.reminders = database()['self_reminders']

    def get_all_reminders(self):
        query = self.reminders.find({}, {"_id": 0})
        reminders = []

        for item in query:
            reminder_element = [item['unique_id'], item['content']]
            reminders.append(reminder_element)

        return reminders

    def add_reminder(self, content):
        query = {
            'unique_id': str(get_random_hex()),
            'content': str(content)
        }

        self.reminders.insert_one(query)

    def find_reminder(self, unique_id):
        query = {
            "unique_id": str(unique_id),
        }

        return self.reminders.find_one(query)

    def delete_reminder(self, unique_id):
        query = {
            'unique_id': unique_id,
        }

        self.reminders.delete_one(query)
