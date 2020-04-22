class ReservationDAO(object):

    # Connection is set here
    def init(self):
        return

    def get_all_reservations(self):
        return [(1, 5, 30, 5), (2, 7, 31, 10), (3, 9, 32, 25)]

    def get_reservation_by_id(self, reservation_id):
        return [
            {
                "reservation_id": 2,
                "customer_id": 7,
                "product_id": 31,
                "reservation_quantity": 10,
            }
        ]

    def get_reservations_by_product_id(self, product_id):
        return [
            {
                "reservation_id": 3,
                "customer_id": 9,
                "product_id": 32,
                "reservation_quantity": 25,
            },
            {
                "reservation_id": 6,
                "customer_id": 3,
                "product_id": 32,
                "reservation_quantity": 8,
            },
        ]

    def get_reservations_by_customer_id(self, customer_id):
        return [
            {
                "reservation_id": 3,
                "customer_id": 9,
                "product_id": 32,
                "reservation_quantity": 25,
            },
            {
                "reservation_id": 7,
                "customer_id": 9,
                "product_id": 19,
                "reservation_quantity": 14,
            },
        ]

    def insert_reservation(self, customer_id, product_id, reservation_quantity):
        reservation_id = 4
        return reservation_id

    def update_reservation(
        self, reservation_id, customer_id, product_id, reservation_quantity
    ):
        reservation_id = 3
        return reservation_id

    def delete_reservation(self, reservation_id):
        return reservation_id
