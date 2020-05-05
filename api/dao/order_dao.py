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

        query = (
                "insert into orders (customer_id, order_total, cc_id)"
                + "values (%s, %s, %s) returning order_id;"
        )
        cursor.execute(query, (customer_id, order_total, cc_id))
        order_id = cursor.fetchone()[0]

        query = ("insert into buys(order_id, product_id, quantity)"
                 + "values (%s, %s, %s);")

        cursor.execute(query, (order_id, product_id, quantity))

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

        query = "delete from buys where order_id = %s;"
        cursor.execute(query, (order_id,))

        query = ("insert into buys(order_id, product_id, quantity)"
                 + "values (%s, %s, %s);")

        cursor.execute(query, (order_id, product_id, quantity))

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

        try:
            current_quantity = cursor.fetchone()[0]
            print("Current Quantity")
            print(current_quantity)
            new_quantity = current_quantity + quantity
            print("New Quantity")
            print(new_quantity)
            query = (
                "update buys set quantity = %s"
                + "where order_id = %s and product_id = %s;"
            )
            cursor.execute(query, (new_quantity, order_id, product_id))

        except TypeError:
            query = ("insert into buys (order_id, product_id, quantity)"
                     + "values (%s, %s, %s);")
            print("In except")
            cursor.execute(query, (order_id, product_id, quantity))

        # Update order_total
        query = "select order_total from orders where order_id = %s;"
        cursor.execute(query, (order_id,))
        new_total = cursor.fetchone()[0] + total
        print("New Total")
        print(new_total)
        query = "update orders set order_total = %s from buys where orders.order_id = %s and product_id = %s returning orders.order_total;"
        cursor.execute(query, (new_total, order_id, product_id))

        order_total = cursor.fetchone()[0]
        print("Order Total")
        print(order_total)

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

        query = "delete from buys where order_id in (select order_id from orders where customer_id = 2);"
        cursor.execute(query, (customer_id,))

        query = "delete from orders where customer_id = %s;"
        cursor.execute(query, (customer_id,))
        self.conn.commit()
