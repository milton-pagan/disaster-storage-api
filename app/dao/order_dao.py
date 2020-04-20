class OrderDAO(object):
    def init(self):
        return

    def get_all_orders(self):
        return [
            (1, 3, 20, 14, 19.99),
            (2, 6, 21, 7, 5.99),
            (3, 5, 22, 45, 50.75),
        ]

    def get_order_by_id(self, order_id):
        return [
            {
                "order_id": 3,
                "customer_id": 5,
                "product_id": 22,
                "order_quantity": 45,
                "order_total": 50.75,
            }
        ]

    def get_orders_by_product_id(self, product_id):
        return [
            {
                "order_id": 3,
                "customer_id": 5,
                "product_id": 22,
                "order_quantity": 45,
                "order_total": 50.75,
            },
            {
                "order_id": 7,
                "customer_id": 9,
                "product_id": 22,
                "order_quantity": 4,
                "order_total": 4.11,
            },
        ]

    def get_orders_by_customer_id(self, customer_id):
        return [
            {
                "order_id": 3,
                "customer_id": 5,
                "product_id": 22,
                "order_quantity": 45,
                "order_total": 50.75,
            },
            {
                "order_id": 15,
                "customer_id": 43,
                "product_id": 22,
                "order_quantity": 11,
                "order_total": 7.75,
            },
        ]

    def insert_order(self, customer_id, product_id, order_quantity, order_total):
        order_id = 4
        return order_id

    def update_order(
        self, customer_id, order_id, product_id, order_quantity, order_total
    ):
        order_id = 3
        return order_id

    def delete_order(self, order_id):
        return order_id
