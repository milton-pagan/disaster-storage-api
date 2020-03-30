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
                "product_id": 20,
                "order_quantity": 14,
                "order_total": 19.99,
            },
            {
                "order_id": 2,
                "product_id": 21,
                "order_quantity": 7,
                "order_total": 5.99,
            },
            {
                "order_id": 3,
                "product_id": 22,
                "order_quantity": 45,
                "order_total": 50.75,
            },
        ]

    def get_order_by_id(self, order_id):
        # if not found in DB return NULL
        return [(1, 19.99)]

    def get_detailed_order_by_id(self, order_id):
        # if not found in DB return NULL
        return [{
                "order_id": 3,
                "product_id": 22,
                "order_quantity": 45,
                "order_total": 50.75,
            }]

    def get_orders_by_product(self, product_id):
        return [(3, 50.75), (7, 4.11)]

    def get_detailed_orders_by_product(self, product_id):
        return [{
                "order_id": 3,
                "product_id": 22,
                "order_quantity": 45,
                "order_total": 50.75,
                },
                {
                "order_id": 7,
                "product_id": 22,
                "order_quantity": 4,
                "order_total": 4.11,
                }]

    def insert_order(self, product_id, order_quantity, order_total):
        order_id = 4
        return order_id

    def update_order(self, order_id, product_id, order_quantity, order_total):
        order_id = 3
        return order_id

    def delete_order(self, order_id):
        return order_id