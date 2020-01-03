from userbot.database import database


class PmPermit:
    def __init__(self):
        self.pm_table = database()['pmpermit']

    def check_if_approved(self, user_id):
        to_check = self.pm_table.find_one({'user_id': user_id})

        if to_check is None:
            self.pm_table.insert_one({'user_id': user_id, 'approval': False})
            return False
        elif to_check['approval'] is False:
            return False
        elif to_check['approval'] is True:
            return True

    def approve(self, user_id):
        if self.check_if_approved(user_id) is True:
            return False
        else:
            self.pm_table.update_one(
                {'user_id': user_id},
                {"$set": {
                    'warn': False,
                    'approval': True,
                    'force_blocked': False,
                    'retard_score': 0,
                }}
            )
            return True

    def block_pm(self, user_id):
        if self.check_if_approved(user_id) is False:
            return False
        else:
            self.pm_table.update_one(
                {'user_id': user_id},
                {
                    "$set": {
                        'warn': True,
                        'approval': False,
                        'force_blocked': True,
                        'retard_score': 10,
                    }
                }
            )
            return True

    def check_if_force_blocked(self, user_id):
        to_check = self.pm_table.find_one({'user_id': user_id})

        if 'force_blocked' not in to_check:
            return False
        elif to_check['force_blocked']:
            return True

    def check_if_warned(self, user_id):
        to_check = self.pm_table.find_one({'user_id': user_id})

        if 'warned' not in to_check:
            self.pm_table.update_one(
                {'user_id': user_id},
                {"$set": {
                    'warned': False
                }}
            )
            return False
        elif to_check['warned'] is False:
            return False
        elif to_check['warned'] is True:
            return True

    def warn(self, user_id):
        if self.check_if_warned(user_id) is True:
            return False
        else:
            self.pm_table.update_one(
                {'user_id': user_id},
                {"$set": {
                    'warned': True
                }}
            )
            return True

    def increment_retard_level(self, user_id):
        if self.check_if_warned(user_id):
            if self.check_if_approved(user_id) is False:
                to_increment = self.pm_table.find_one({'user_id': user_id})

                if 'retard_score' not in to_increment:
                    self.pm_table.update_one(
                        {'user_id': user_id},
                        {"$set": {
                            'retard_score': 1
                        }}
                    )
                elif 'retard_score' in to_increment:
                    self.pm_table.update_one(
                        {'user_id': user_id},
                        {"$inc": {
                            'retard_score': 1
                        }}
                    )

    def calculate_retard_level(self, user_id):
        if self.check_if_warned(user_id):
            if self.check_if_approved(user_id) is False:
                to_calculate = self.pm_table.find_one({'user_id': user_id})

                if 'retard_score' not in to_calculate:
                    return 0
                elif 'retard_score' in to_calculate:
                    return to_calculate['retard_score']
