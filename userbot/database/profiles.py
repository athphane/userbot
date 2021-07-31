from userbot.database import database


class Profiles:
    def __init__(self):
        self.profiles = database()["profiles"]

    def all_profiles(self):
        return self.profiles.find()

    def add_profile(self, channel_id, title, username):
        data = {
            'channel_id': channel_id,
            'username': username,
            'title': title
        }
        self.profiles.insert_one(data)

    def getProfile(self, idx):
        # profiles = list(self.profiles.find())
        profiles = self.profiles.find()
        try:
            for i, x in enumerate(profiles):
                if i == idx - 1:
                    return x
        except Exception:
            return None
