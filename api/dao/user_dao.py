import psycopg2


class UserDAO(object):
    def init(self):
        return

    def get_all_users(self):
        return [
            (1, "dionel.martinez", "dionil1234", 7877775555),
            (2, "milton.pagan1", "malta4321", 7877774444),
            (3, "jesus.garcia13", "jishu1324", 7877773333),
        ]

    def get_user_by_id(self, user_id):
        return [(2, "milton.pagan1", "malta4321", 7877774444)]

    def insert_user(self, username, password, phone):
        return 1

    def update_user(self, user_id, username, password, phone):
        return user_id

    def delete_user(self, user_id):
        return user_id
