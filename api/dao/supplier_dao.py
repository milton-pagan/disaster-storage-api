import psycopg2
import psycopg2.extras
from api.config.config import get_config

class SupplierDAO(object):

    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    # General Supplier Operations

    def get_all_suppliers(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT user_id, username, phone, supplier_id, supplier_name, supplier_city, location_id FROM supplier ORDER BY supplier_id;"
        cursor.execute(query)

        return cursor.fetchall()

    def get_suppliers_by_city(self, supplier_city):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT supplier_name FROM supplier WHERE supplier_city=%s ORDER BY supplier_id;"
        cursor.execute(query, (supplier_city,))

        return cursor.fetchall()

    # Operations using Supplier Id

    def get_supplier_by_id(self, supplier_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT user_id, username, phone, supplier_id, supplier_name, supplier_city, location_id FROM supplier WHERE supplier_id=%s ORDER BY supplier_id;"
        cursor.execute(query, (supplier_id,))

        return cursor.fetchone()

    def get_products_by_supplier_id(self, supplier_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT product_name, product_id FROM product NATURAL INNER JOIN supplies WHERE supplier_id=%s ORDER BY product_name;"
        cursor.execute(query, (supplier_id,))

        return cursor.fetchall()

    def get_supplier_location(self, supplier_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT latitude, longitude FROM location WHERE location_id = (SELECT location_id FROM supplier WHERE supplier_id=%s);"
        cursor.execute(query, (supplier_id,))

        return cursor.fetchone()

    def insert_supplier(self, username, password, phone, supplier_name, supplier_city, location_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO supplier(username, password, phone, supplier_name, supplier_city, location_id)"\
                +"VALUES (%s, %s, %s, %s, %s, %s) returning supplier_id;"
        cursor.execute(
            query,
            (
                username,
                password,
                phone,
                supplier_name,
                supplier_city,
                location_id,
            ),
        )
        supplier_id = cursor.fetchone()[0]
        self.conn.commit()
        return supplier_id

    def insert_supplies_product_by_supplier_id(self, supplier_id, product_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO supplies(supplier_id, product_id) VALUES (%s, %s);"
        cursor.execute(
            query,
            (
                supplier_id,
                product_id,
            ),
        )
        self.conn.commit()
        return supplier_id, product_id

    def update_supplier(self, supplier_id, supplier_name, supplier_city, location_id):
        return supplier_id, location_id

    def delete_supplier(self, supplier_id):
        return supplier_id
