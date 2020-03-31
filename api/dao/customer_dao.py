import psycopg2


class CustomerDAO(object):
    def __init__(self):
        return

    # General Customer Operations

    def get_all_customer(self):
        return [
            (1, "Dionel", "Martinez", "Santa Isabel", 3),
            (2, "Milto", "Pagan", "Juana Diaz", 7),
            (3, "Jesus", "Garcia", "San Juan", 8)
        ]

    def get_customers_by_city(self, customer_city):
        return [(1, "Dionel", "Martinez", "Santa Isabel", 3)]

    # Operations using Customer Id

    def get_customer_by_id(self, customer_id):
        return [(1, "Dionel", "Martinez", "Santa Isabel", 3)]

    def insert_customer(
            self,
            customer_first_name,
            customer_last_name,
            customer_city,
            location_id,
            cc_id,
            user_id
    ):
        customer_id = 9
        return customer_id

    def update_customer(
            self,
            customer_id,
            customer_first_name,
            customer_last_name,
            customer_city,
            location_id
    ):
        return customer_id, location_id

    def delete_customer(self, customer_id):
        return customer_id
