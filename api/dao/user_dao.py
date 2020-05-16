import psycopg2
import psycopg2.extras
from api.config.config import get_config


class UserDAO(object):

    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    # General User Operations

    def get_all_users(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM public.user ORDER BY user_id"
        cursor.execute(query)

        return cursor.fetchall()

    # Operations by user_id

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM public.user WHERE user_id = %s;"
        cursor.execute(query, (user_id,))

        return cursor.fetchone()

    # Update Operations for User

    def insert_user(self, username, password, phone):
        cursor = self.conn.cursor()
        query = "INSERT INTO public.user(username, password, phone) VALUES (%s, %s, %s) returning user_id;"
        cursor.execute(query, (username, password, phone),)
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id

    def update_user(self, user_id, username, password, phone):
        cursor = self.conn.cursor()
        query = "UPDATE public.user SET username=%s, password=%s, phone=%s WHERE user_id=%s;"
        cursor.execute(query, (username, password, phone, user_id), )
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id

    def delete_user(self, user_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM public.user WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        self.conn.commit()

        return user_id
