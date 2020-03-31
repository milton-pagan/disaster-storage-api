import psycopg2

class AdminDAO(object):

    def __init__(self):
        return

    def get_all_admins(self):
        return [(1, "NombreAdmin1"),
                (2, "NombreAdmin2")]

    def get_admin_by_id(self, admin_id):
        return [(2, "NombreAdmin2")]

    def insert_admin(self, admin_name):
        admin_id = 3
        return admin_id