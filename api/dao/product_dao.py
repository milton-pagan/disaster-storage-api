import psycopg2
import psycopg2.extras
from api.config.config import get_config


class ProductDAO(object):
    # Connection to backend is set up here
    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    # General product operations

    def get_all_products(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from product order by product_id;"
        cursor.execute(query)

        return cursor.fetchall()

    def get_products_by_category(self, category):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = "select * from product natural inner join " + category + " order by product_id;"
        cursor.execute(query)

        return cursor.fetchall()

    # Operations by product id

    def get_product_by_id(self, product_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from product where product_id= %s;"
        cursor.execute(query, (product_id,))

        return cursor.fetchone()

    def get_detailed_product_by_id(self, product_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = "select product_category from product where product_id= %s;"
        cursor.execute(query, (product_id,))
        category = cursor.fetchone()["product_category"]

        query = (
            "select * from product natural inner join "
            + category
            + " where product_id= %s;"
        )
        cursor.execute(query, (product_id,))

        return cursor.fetchall()

    def get_product_location(self, product_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = "select latitude, longitude from location natural inner join product where product_id= %s;"
        cursor.execute(query, (product_id,))

        return cursor.fetchall()

    def get_product_location_id(self, product_id):
        cursor = self.conn.cursor()

        query = "select location_id from product where product_id= %s;"
        cursor.execute(query, (product_id,))

        return cursor.fetchone()[0]

    def get_product_category(self, product_id):
        cursor = self.conn.cursor()

        query = "select product_category from product where product_id= %s;"
        cursor.execute(query, (product_id,))

        return cursor.fetchone()[0]

    def get_products_by_keyword(self, keyword):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = "select * from product where product_name ilike %s order by product_name;"
        keyword = "%" + keyword + "%"
        cursor.execute(query, (keyword,))

        return cursor.fetchall()

    def insert_product(
        self,
        product_name,
        product_quantity,
        product_price,
        product_description,
        product_category,
        location_id,
    ):
        cursor = self.conn.cursor()
        query = (
            "insert into product(product_name, product_quantity, product_price, product_description, product_category, location_id)"
            + "values (%s, %s, %s, %s, %s, %s) returning product_id;"
        )
        cursor.execute(
            query,
            (
                product_name,
                product_quantity,
                product_price,
                product_description,
                product_category,
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
        product_category,
        product_description,
    ):
        cursor = self.conn.cursor()
        query = (
            "update product set product_name = %s, product_quantity = %s, product_price = %s,"
            + "product_category = %s, product_description = %s where product_id = %s returning location_id;"
        )
        cursor.execute(
            query,
            (
                product_name,
                product_quantity,
                product_price,
                product_category,
                product_description,
                product_id,
            ),
        )

        location_id = cursor.fetchone()[0]
        self.conn.commit()

        return location_id

    def delete_product(self, product_id):
        cursor = self.conn.cursor()
        query = "delete from product where product_id = %s returning location_id;"
        cursor.execute(query, (product_id,))
        location_id = cursor.fetchone()[0]
        self.conn.commit()

        return location_id
