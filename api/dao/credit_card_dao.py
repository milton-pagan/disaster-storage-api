import psycopg2
import psycopg2.extras
from api.config.config import get_config

class CreditCardDAO(object):
    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    def insert_credit_card(self, cc_type, cc_number, customer_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO credit_card(cc_type, cc_number, customer_id) VALUES (%s, %s, %s) returning cc_id;"
        cursor.execute(query, (cc_type, cc_number, customer_id))
        cc_id = cursor.fetchone()[0]
        self.conn.commit()

        return cc_id

    def update_credit_card(self, cc_id, cc_type, cc_number, customer_id):
        return cc_id, customer_id
