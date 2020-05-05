import psycopg2
from api.config.config import get_config

class ReservationDAO(object):

    # Connection is set here
    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    def get_all_reservations(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from reservation natural inner join reserves order by reservation_id;"
        cursor.execute(query)

        return cursor.fetchall()

    def get_reservation_by_id(self, reservation_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = ("select * from reservation natural inner join reserves "
                 + "where reservation_id= %s order by reservation_id;")
        cursor.execute(query, (reservation_id,))

        return cursor.fetchall()

    def get_reservations_by_product_id(self, product_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select * from reservation natural inner join reserves where product_id= %s order by reservation_id;"
        cursor.execute(query, (product_id,))

        return cursor.fetchall()

    def get_reservations_by_customer_id(self, customer_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = ("select * from reservation natural inner join reserves "
                 + "where customer_id= %s order by reservation_id;")
        cursor.execute(query, (customer_id,))

        return cursor.fetchall()

    def insert_reservation(self, customer_id, product_id, quantity):
        cursor = self.conn.cursor()

        query = "select product_price from product where product_id = %s;"
        cursor.execute(query, (product_id,))
        try:
            price = cursor.fetchone()[0]
            if price > 0:
                return -2
        except TypeError:
            return -1

        query = (
                "insert into reservation (customer_id)"
                + "values (%s) returning reservation_id;"
        )
        cursor.execute(query, (customer_id,))

        reservation_id = cursor.fetchone()[0]

        query = ("insert into reserves(reservation_id, product_id, quantity)"
                 + "values (%s, %s, %s);")
        cursor.execute(query, (reservation_id, product_id, quantity))

        self.conn.commit()
        return reservation_id

    def update_reservation(
        self, reservation_id, customer_id, product_id, quantity
    ):
        cursor = self.conn.cursor()

        query = "select product_price from product where product_id = %s;"
        cursor.execute(query, (product_id,))
        try:
            price = cursor.fetchone()[0]
            if price > 0:
                return -2
        except TypeError:
            return -1

        query = "delete from reserves where reservation_id = %s;"
        cursor.execute(query, (reservation_id,))

        query = ("insert into reserves(reservation_id, product_id, quantity)"
                 + "values (%s, %s, %s);")

        cursor.execute(query, (reservation_id, product_id, quantity))

        query = (
                "update reservation set customer_id = %s"
                + "where reservation_id = %s returning reservation_id;"
        )

        cursor.execute(query, (customer_id,reservation_id))
        reservation_id_out = cursor.fetchone()[0]

        self.conn.commit()

        return reservation_id_out

    def add_product(self, reservation_id, product_id, quantity):
        cursor = self.conn.cursor()

        query = "select product_price from product where product_id = %s;"
        cursor.execute(query, (product_id,))
        try:
            price = cursor.fetchone()[0]
            if price > 0:
                return -2
        except TypeError:
            return -1

        query = "select quantity from reserves where reservation_id = %s and product_id = %s;"
        cursor.execute(query, (reservation_id, product_id))

        try:
            current_quantity = cursor.fetchone()[0]
            new_quantity = current_quantity + quantity
            query = (
                    "update reserves set quantity = %s"
                    + "where reservation_id = %s and product_id = %s;"
            )
            cursor.execute(query, (new_quantity, reservation_id, product_id))

        except TypeError:
            query = ("insert into reserves (reservation_id, product_id, quantity)"
                     + "values (%s, %s, %s);")
            cursor.execute(query, (reservation_id, product_id, quantity))
            new_quantity = quantity

        self.conn.commit()

        return new_quantity

    def delete_reservation(self, reservation_id):
        cursor = self.conn.cursor()

        query = "delete from reserves where reservation_id = %s;"
        cursor.execute(query, (reservation_id,))

        query = "delete from reservation where reservation_id = %s;"
        cursor.execute(query, (reservation_id,))
        self.conn.commit()

    def delete_reservations_by_customer_id(self, customer_id):
        cursor = self.conn.cursor()

        query = "delete from reserves where reservation_id in (select reservation_id from reservation where customer_id = %s);"
        cursor.execute(query, (customer_id,))

        query = "delete from reservation where customer_id = %s;"
        cursor.execute(query, (customer_id,))
        self.conn.commit()

