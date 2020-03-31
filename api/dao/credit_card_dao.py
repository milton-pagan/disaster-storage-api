import psycopg2

class CreditCardDAO(object):

    def __init__(self):
        return

    def insert_credit_card(self, cc_type, cc_number, customer_id):
        cc_id = 1
        return cc_id

    def update_credit_card(self, cc_id, cc_type, cc_number, customer_id):
        return cc_id, customer_id
