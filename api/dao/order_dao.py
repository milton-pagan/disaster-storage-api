import psycopg2

from api.config.config import get_config


class OrderDAO(object):
    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    def get_all_orders(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from orders natural inner join buys order by order_id;"
        cursor.execute(query)

        return cursor.fetchall()

    def get_order_by_id(self, order_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from orders natural inner join buys where order_id= %s order by order_id;"
        cursor.execute(query, (order_id,))

        return cursor.fetchall()

    def get_orders_by_product_id(self, product_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from orders natural inner join buys where product_id= %s order by product_id;"
        cursor.execute(query, (product_id,))

        return cursor.fetchall()

    def get_orders_by_customer_id(self, customer_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from orders natural inner join buys where customer_id= %s;"
        cursor.execute(query, (customer_id,))

        return cursor.fetchall()

    def insert_order(self, customer_id, product_id, quantity, order_total):
        cursor = self.conn.cursor()

        query = "select cc_id from customer natural inner join credit_card where customer_id = %s;"
        cursor.execute(query, (customer_id,))

        try:
            cc_id = cursor.fetchone()[0]
        except TypeError:
            return -1

        query = "select product_price from product where product_id = %s;"
        cursor.execute(query, (product_id,))

        try:
            price = cursor.fetchone()[0]
            if price == 0:
                return -3
        except TypeError:
            return -2

        # Verify product_quantity
        query = "select product_quantity from product where product_id = %s;"
        cursor.execute(query, (product_id,))
        try:
            current_quantity = cursor.fetchone()[0]
            if current_quantity - quantity < 0:
                return -4
        except TypeError:
            return -2

        query = (
                "insert into orders (customer_id, order_total, cc_id)"
                + "values (%s, %s, %s) returning order_id;"
        )
        cursor.execute(query, (customer_id, order_total, cc_id))
        order_id = cursor.fetchone()[0]

        query = ("insert into buys(order_id, product_id, quantity)"
                 + "values (%s, %s, %s);")

        cursor.execute(query, (order_id, product_id, quantity))

        # Update product_quantity
        new_quantity = current_quantity - quantity
        query = "update product set product_quantity = %s where product_id = %s;"
        cursor.execute(query, (new_quantity, product_id))

        self.conn.commit()
        return order_id

    def update_order(
        self, customer_id, order_id, product_id, quantity, order_total
    ):
        cursor = self.conn.cursor()

        query = "select cc_id from customer natural inner join credit_card where customer_id = %s;"
        cursor.execute(query, (customer_id,))

        try:
            cc_id = cursor.fetchone()[0]
        except TypeError:
            return -1

        query = "select product_price from product where product_id = %s;"
        cursor.execute(query, (product_id,))

        try:
            price = cursor.fetchone()[0]
            if price == 0:
                return -3
        except TypeError:
            return -2

        query = "select product_id from buys where order_id = %s;"
        cursor.execute(query, (order_id,))

        # Return products to storage
        old_product_id = cursor.fetchone()[0]

        query = "select quantity from buys where product_id = %s and order_id = %s;"
        cursor.execute(query, (old_product_id, order_id))

        previous_quantity = cursor.fetchone()[0]

        query = "select product_quantity from product where product_id = %s;"
        cursor.execute(query, (old_product_id,))
        current_qty = cursor.fetchone()[0]

        query = "update product set product_quantity = %s where product_id = %s;"
        cursor.execute(query, (current_qty + previous_quantity, old_product_id))

        # Verify product_quantity
        query = "select product_quantity from product where product_id = %s;"
        cursor.execute(query, (product_id,))
        try:
            current_quantity = cursor.fetchone()[0]
            if current_quantity - quantity < 0:
                return -4
        except TypeError:
            return -2

        # Update order
        query = "delete from buys where order_id = %s;"
        cursor.execute(query, (order_id,))

        query = ("insert into buys(order_id, product_id, quantity)"
                 + "values (%s, %s, %s);")

        cursor.execute(query, (order_id, product_id, quantity))

        # Discount products from storage
        new_quantity = current_quantity - quantity
        query = "update product set product_quantity = %s where product_id = %s;"
        cursor.execute(query, (new_quantity, product_id))

        query = (
                "update orders set customer_id = %s, cc_id = %s, order_total = %s"
                + "where order_id = %s returning order_id;"
        )

        cursor.execute(query, (customer_id, cc_id, order_total, order_id))
        order_id_out = cursor.fetchone()[0]

        self.conn.commit()

        return order_id_out

    def add_product(self, order_id, product_id, quantity, total):
        cursor = self.conn.cursor()

        query = "select product_price from product where product_id = %s;"
        cursor.execute(query, (product_id,))

        try:
            price = cursor.fetchone()[0]
            if price == 0:
                return -3
        except TypeError:
            return -2

        query = "select quantity from buys where order_id = %s and product_id = %s;"
        cursor.execute(query, (order_id, product_id))

        # Verify new product quantity
        try:
            current_quantity = cursor.fetchone()[0]
            new_quantity = current_quantity + quantity

            query = (
                "update buys set quantity = %s"
                + "where order_id = %s and product_id = %s;"
            )
            cursor.execute(query, (new_quantity, order_id, product_id))

        except TypeError:
            new_quantity = quantity
            query = ("insert into buys (order_id, product_id, quantity)"
                     + "values (%s, %s, %s);")
            cursor.execute(query, (order_id, product_id, quantity))

        # Verify DB product_quantity
        query = "select product_quantity from product where product_id = %s;"
        cursor.execute(query, (product_id,))
        try:
            db_current_quantity = cursor.fetchone()[0]
            if db_current_quantity < new_quantity:
                return -4
        except TypeError:
            pass

        # Update order_total
        query = "select order_total from orders where order_id = %s;"
        cursor.execute(query, (order_id,))
        new_total = cursor.fetchone()[0] + total
        query = "update orders set order_total = %s from buys where orders.order_id = %s and product_id = %s returning orders.order_total;"
        cursor.execute(query, (new_total, order_id, product_id))

        order_total = cursor.fetchone()[0]

        # Discount products from storage
        db_new_quantity = db_current_quantity - quantity
        query = "update product set product_quantity = %s where product_id = %s;"
        cursor.execute(query, (db_new_quantity, product_id))

        self.conn.commit()

        return order_total

    def delete_order(self, order_id):
        cursor = self.conn.cursor()

        query = "delete from buys where order_id = %s;"
        cursor.execute(query, (order_id,))

        query = "delete from orders where order_id = %s;"
        cursor.execute(query, (order_id,))
        self.conn.commit()

    def delete_order_by_customer_id(self, customer_id):
        cursor = self.conn.cursor()

        query = "delete from buys where order_id in (select order_id from orders where customer_id = %s);"
        cursor.execute(query, (customer_id,))

        query = "delete from orders where customer_id = %s;"
        cursor.execute(query, (customer_id,))
        self.conn.commit()
