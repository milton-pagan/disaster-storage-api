import psycopg2
import psycopg2.extras
from api.config.config import get_config

class AdminDAO(object):
    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    def get_all_admins(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT user_id, username, phone, admin_id, admin_name FROM public.admin NATURAL INNER JOIN public.user ORDER BY admin_id;"
        cursor.execute(query)

        return cursor.fetchall()

    def get_admin_by_id(self, admin_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT user_id, username, phone, admin_id, admin_name FROM public.admin NATURAL INNER JOIN public.user WHERE admin_id=%s;"
        cursor.execute(query, (admin_id,))

        return cursor.fetchone()

    def insert_admin(self, admin_name, user_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO admin(admin_name, user_id) VALUES (%s, %s) returning admin_id;"
        cursor.execute(query, (admin_name, user_id))
        admin_id = cursor.fetchone()[0]
        self.conn.commit()
        return admin_id

    def update_admin(self, admin_id, admin_name):
        cursor = self.conn.cursor()
        query = "UPDATE admin SET admin_name=%s WHERE admin_id=%s;"
        cursor.execute(query, (admin_name, admin_id,))
        admin_id = cursor.fetchone()[0]
        self.conn.commit()
        return admin_id

    def delete_admin(self, admin_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM admin WHERE admin_id = %s;"
        cursor.execute(query, (admin_id,))
        self.conn.commit()

        return admin_id
