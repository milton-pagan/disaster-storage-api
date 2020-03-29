class OrderDAO(object):

    def init(self):
        return

    def get_all_orders(self):
        # id, price
        return [
            (1, 19.99),
            (2, 5.99),
            (3, 50.75)
        ]

    def get_all_detailed_orders(self):
        # id, quantity, price
        return [
            {
                "order_id": 1,
                "order_quantity": 14,
                "order_total": 19.99,
            },
            {
                "order_id": 2,
                "order_quantity": 7,
                "order_total": 5.99,
            },
            {
                "order_id": 3,
                "order_quantity": 45,
                "order_total": 50.75,
            },
        ]

    def get_order_by_id(self, order_id):
        # if not found in DB return NULL
        return [(1, 19.99)]

    def insert_order(self, order_quantity, order_total):
        order_id = 4
        return order_id

    def update_product(self, order_id, order_quantity, order_total):
        order_id = 3
        return order_id

    def delete_product(self, order_id):
        return order_id