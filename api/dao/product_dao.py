import psycopg2
import psycopg2.extras
from api.config.config import get_config
from api.dao.category_info import categories


class ProductDAO(object):
    # Connection to backend is set up here
    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    # General product operations

    def get_all_products(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from product;"
        cursor.execute(query)

        return cursor.fetchall()

    def get_all_detailed_products(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # TODO: FIX
        query = "select * from product" + "".join(["," + category for category in categories.keys()]) + ",location;"
        cursor.execute(query)

        return cursor.fetchall()

    def get_products_by_category(self, category):
        return [
            {
                "product_id": 1,
                "product_name": "water bottle",
                "product_quantity": 100,
                "product_price": 0.0,
                "product_description": "bottle of water",
                "location_id": 1,
                "exp_date": "2020-06-22",
                "volume_ml": 500,
                "location_latitude": 18.20985,
                "location_longitude": -67.13918,
            }
        ]

    # Operations by product id

    def get_product_by_id(self, product_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from product where product_id=%s"
        cursor.execute(query, (product_id,))

        return cursor.fetchone()

    def get_detailed_product_by_id(self, product_id):
        return [
            {
                "product_id": 1,
                "product_name": "water bottle",
                "product_quantity": 100,
                "product_price": 0.0,
                "product_description": "bottle of water",
                "location_id": 1,
                "exp_date": "2020-06-22",
                "volume_ml": 500,
                "location_latitude": 18.20985,
                "location_longitude": -67.13918,
            }
        ]

    def get_products_by_name(self, product_name):
        # TODO: Query by name and sort by name
        return [(3, "ibuprofen", 20, 4.0, "generic", 1)]

    def insert_product(
        self,
        product_name,
        product_quantity,
        product_price,
        product_description,
        location_id,
    ):
        cursor = self.conn.cursor()
        query = "insert into product(product_name, product_quantity, product_price, product_description, location_id) values (%s, %s, %s, %s, %s) returning product_id;"
        cursor.execute(
            query,
            (
                product_name,
                product_quantity,
                product_price,
                product_description,
                location_id,
            ),
        )
        product_id = cursor.fetchone()[0]
        self.conn.commit()
        return product_id

    def update_product(
        self,
        product_id,
        product_name,
        product_quantity,
        product_price,
        product_description,
    ):
        cursor = self.conn.cursor()
        query = "update product set product_name = %s, product_quantity = %s, product_price = %s, product_description = %s where product_id = %s returning location_id;"
        cursor.execute(
            query,
            (
                product_name,
                product_quantity,
                product_price,
                product_description,
                product_id,
            ),
        )

        location_id = cursor.fetchone()[0]  # Must return location id to update it
        self.conn.commit()

        return location_id

    def delete_product(self, product_id):
        cursor = self.conn.cursor()
        query = "delete from product where product_id = %s returning location_id;"
        cursor.execute(query, (product_id,))
        location_id = cursor.fetchone()[0]
        self.conn.commit()

        return location_id
