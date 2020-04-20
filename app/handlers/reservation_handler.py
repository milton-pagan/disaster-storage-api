from app.dao.reservation_dao import ReservationDAO
from app.handlers.error_handler import ErrorHandler
from flask import jsonify


class ReservationHandler(object):
    def build_reservation(self, record):
        res_dict = {
            "reservation_id": record[0],
            "customer_id": record[1],
            "product_id": record[2],
            "reservation_quantity": record[3],
        }
        return res_dict

    def get_all_reservations(self):
        result = ReservationDAO().get_all_reservations()
        res_dict = []
        for reservation in result:
            res_dict.append(self.build_reservation(reservation))
        return jsonify(reservations=res_dict)

    def get_reservation_by_id(self, reservation_id):
        result = ReservationDAO().get_reservation_by_id(reservation_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(reservation=result), 200

    def get_reservations_by_product_id(self, product_id):
        results = ReservationDAO().get_reservations_by_product_id(product_id)
        if not results:
            return ErrorHandler().not_found()
        return jsonify(reservations=results), 200

    def get_reservations_by_customer_id(self, customer_id):
        results = ReservationDAO().get_reservations_by_customer_id(customer_id)
        if not results:
            return ErrorHandler().not_found()
        return jsonify(reservations=results), 200

    def insert_reservation(self, payload):
        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            reservation_quantity = payload["reservation_quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        reservation_id = ReservationDAO().insert_reservation(
            customer_id, product_id, reservation_quantity
        )
        return (
            self.build_reservation(
                (reservation_id, customer_id, product_id, reservation_quantity)
            ),
            201,
        )

    def update_reservation(self, reservation_id, payload):
        if not self.get_reservation_by_id(reservation_id):
            return ErrorHandler().not_found()

        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            reservation_quantity = payload["reservation_quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        dao = ReservationDAO()
        reservation_id = dao.update_reservation(
            reservation_id, customer_id, product_id, reservation_quantity
        )
        return (
            self.build_reservation(
                (reservation_id, customer_id, product_id, reservation_quantity)
            ),
            200,
        )

    def delete_reservation(self, reservation_id):
        if not self.get_reservation_by_id(reservation_id):
            return ErrorHandler().not_found()
        else:
            ReservationDAO().delete_reservation(reservation_id)
            return jsonify(Deletion="Deleted"), 200
