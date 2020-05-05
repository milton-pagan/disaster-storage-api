import psycopg2
from api.config.config import get_config

class RequestDAO(object):

    """ Connection is set here """
    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    def get_all_requests(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from request natural inner join requests order by request_id;"
        cursor.execute(query)

        return cursor.fetchall()

    def get_request_by_id(self, request_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = ("select * from request natural inner join requests "
                 + "where request_id= %s order by request_id;")
        cursor.execute(query, (request_id,))

        return cursor.fetchall()

    def get_requests_by_product_id(self, product_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from request natural inner join requests where product_id= %s order by request_id;"
        cursor.execute(query, (product_id,))

        return cursor.fetchall()

    def get_requests_by_customer_id(self, customer_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = ("select * from request natural inner join requests "
                 + "where customer_id= %s order by request_id;")
        cursor.execute(query, (customer_id,))

        return cursor.fetchall()

    def get_requests_by_keyword(self, keyword):
        """ Search for keyword = Product Name
            Result: Orders joined with Products that match
        """
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = (
            "select * from request natural inner join product where product_name ilike %s order by product_name;"
        )
        keyword = "%" + keyword + "%"
        cursor.execute(query, (keyword,))

        return cursor.fetchall()

    def insert_request(self, customer_id, product_id, quantity):
        cursor = self.conn.cursor()

        query = "select * from product where product_id = %s;"
        cursor.execute(query, (product_id,))

        try:
            exists = cursor.fetchone()[0]
        except TypeError:
            return -1

        query = (
                "insert into request (customer_id)"
                + "values (%s) returning request_id;"
        )
        cursor.execute(query, (customer_id,))

        request_id = cursor.fetchone()[0]

        query = ("insert into requests (request_id, product_id, quantity)"
                 + "values (%s, %s, %s);")
        cursor.execute(query, (request_id, product_id, quantity))

        self.conn.commit()
        return request_id

    def update_request(self, request_id, customer_id, product_id, quantity):
        cursor = self.conn.cursor()

        query = "select * from product where product_id = %s;"
        cursor.execute(query, (product_id,))

        try:
            exists = cursor.fetchone()[0]
        except TypeError:
            return -1

        query = "delete from requests where request_id = %s;"
        cursor.execute(query, (request_id,))

        query = ("insert into requests (request_id, product_id, quantity)"
                 + "values (%s, %s, %s);")

        cursor.execute(query, (request_id, product_id, quantity))

        query = (
                "update request set customer_id = %s"
                + "where request_id = %s returning request_id;"
        )

        cursor.execute(query, (customer_id, request_id))
        request_id_out = cursor.fetchone()[0]

        self.conn.commit()

        return request_id_out

    def add_product(self, request_id, product_id, quantity):
        cursor = self.conn.cursor()

        query = "select * from product where product_id = %s;"
        cursor.execute(query, (product_id,))

        try:
            price = cursor.fetchone()[0]
        except TypeError:
            return -1

        query = "select quantity from requests where request_id = %s and product_id = %s;"
        cursor.execute(query, (request_id, product_id))

        try:
            current_quantity = cursor.fetchone()[0]
            new_quantity = current_quantity + quantity
            query = (
                    "update requests set quantity = %s"
                    + "where request_id = %s and product_id = %s;"
            )
            cursor.execute(query, (new_quantity, request_id, product_id))

        except TypeError:
            query = ("insert into requests (request_id, product_id, quantity)"
                     + "values (%s, %s, %s);")
            cursor.execute(query, (request_id, product_id, quantity))
            new_quantity = quantity

        self.conn.commit()

        return new_quantity

    def delete_request(self, request_id):
        cursor = self.conn.cursor()

        query = "delete from requests where request_id = %s;"
        cursor.execute(query, (request_id,))

        query = "delete from request where request_id = %s;"
        cursor.execute(query, (request_id,))
        self.conn.commit()

    def delete_requests_by_customer_id(self, customer_id):
        cursor = self.conn.cursor()

        query = "delete from requests where request_id in (select request_id from request where customer_id = %s);"
        cursor.execute(query, (customer_id,))

        query = "delete from request where customer_id = %s;"
        cursor.execute(query, (customer_id,))
        self.conn.commit()
