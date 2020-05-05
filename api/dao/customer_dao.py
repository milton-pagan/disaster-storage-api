import psycopg2
import psycopg2.extras
from api.config.config import get_config

class CustomerDAO(object):
    def __init__(self):
        return

    # General Customer Operations

    def get_all_customer(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT user_id, username, phone, customer_id, customer_first_name, customer_last_name, customer_city, location_id FROM customer NATURAL INNER JOIN PUBLIC.USER ORDER BY customer_id;"
        cursor.excecute(query)

        return cursor.fetchall()

    def get_customers_by_city(self, customer_city):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT customer_id, customer_name FROM customer WHERE customer_city=%s ORDER BY customer_id"
        cursor.excecute(query, (customer_city,))

        return cursor.fetchall()

    # Operations using Customer Id

    def get_customer_by_id(self, customer_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT user_id, username, phone, customer_id, customer_first_name, customer_last_name, customer_city, location_id FROM customer NATURAL INNER JOIN PUBLIC.USER WHERE customer_id=%s ORDER BY customer_id"
        cursor.excecute(query, (customer_id,))

        return cursor.fetchone()

    def get_customer_location_by_id(self, customer_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT latitude, longitude FROM location NATURAL INNER JOIN customer WHERE customer_id=%s;"
        cursor.excecute(query, (customer_id,))

        return cursor.fetchall()

    # Operations that return the products names
    # that (order, reserve or request) a specific customer

    def get_product_ordered_by_customer(self, customer_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT product_name FROM orders NATURAL INNER JOIN buys NATURAL INNER JOIN product WHERE customer_id=%s;"
        cursor.excecute(query, (customer_id,))

        return cursor.fetchall()

    def get_product_reserved_by_customer(self, customer_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT product_name FROM orders NATURAL INNER JOIN reserves NATURAL INNER JOIN product WHERE customer_id=%s;"
        cursor.excecute(query, (customer_id,))

        return cursor.fetchall()

    def get_product_requested_by_customer(self, customer_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT product_name FROM orders NATURAL INNER JOIN request NATURAL INNER JOIN product WHERE customer_id=%s;"
        cursor.excecute(query, (customer_id,))

        return cursor.fetchall()

    def insert_customer(
        self,
        customer_first_name,
        customer_last_name,
        customer_city,
        location_id,
        cc_id,
        user_id,
    ):
        customer_id = 9
        return customer_id

    def update_customer(
        self,
        customer_id,
        customer_first_name,
        customer_last_name,
        customer_city,
        location_id,
    ):
        return customer_id, location_id

    def delete_customer(self, customer_id):
        return customer_id
