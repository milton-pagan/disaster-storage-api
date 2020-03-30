class ReservationDAO(object):

    # Connection is set here
    def init(self):
        return

    def get_all_reservations(self):
        # reservation_id, product_id
        return [
            (1, 30),
            (2, 31),
            (3, 32)
        ]

    def get_all_detailed_reservations(self):
        # reservation_id, product_id, quantity
        return [
            {
                "reservation_id": 1,
                "product_id": 30,
                "reservation_quantity": 5,

            },
            {
                "reservation_id": 2,
                "product_id": 31,
                "reservation_quantity": 10,
            },
            {
                "reservation_id": 3,
                "product_id": 32,
                "reservation_quantity": 25,

            },
        ]

    def get_reservation_by_id(self, reservation_id):
        return [(1, 30)]

    def get_detailed_reservation_by_id(self, reservation_id):
        return [{
                "reservation_id": 2,
                "product_id": 31,
                "reservation_quantity": 10
                }]

    def get_reservations_by_product(self, product_id):
        return [(3, 32), (6, 12)]

    def get_detailed_reservations_by_product(self, product_id):
        return [{
                "reservation_id": 3,
                "product_id": 32,
                "reservation_quantity": 25,
                },
                {
                "reservation_id": 6,
                "product_id": 12,
                "reservation_quantity": 8,
                }]

    def insert_reservation(self, product_id, reservation_quantity):
        reservation_id = 4
        return reservation_id

    def update_reservation(self, reservation_id, product_id, reservation_quantity):
        reservation_id = 3
        return reservation_id

    def delete_reservation(self, reservation_id):
        return reservation_id
