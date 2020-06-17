from userbot.database import database


class Settings:
    def __init__(self):
        self.pm_table = database()['settings']

    def set_pm_permit(self, status: bool):
        self.pm_table.update_one({'key': 'pm_permit', 'value': status}, '')
