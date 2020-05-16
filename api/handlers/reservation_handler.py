from api.dao.reservation_dao import ReservationDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class ReservationHandler(object):
    def build_reservation(self, record):
        res_dict = {
            "reservation_id": record[0],
            "customer_id": record[1],
            "product_id": record[2],
            "quantity": record[3],
        }
        return res_dict

    def get_all_reservations(self):
        results = ReservationDAO().get_all_reservations()
        return jsonify(reservations=results)

    def get_reservation_by_id(self, reservation_id):
        results = ReservationDAO().get_reservation_by_id(reservation_id)
        if not results:
            return ErrorHandler().not_found()
        return jsonify(reservation=results), 200

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
            quantity = payload["quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        reservation_id = ReservationDAO().insert_reservation(
            customer_id, product_id, quantity
        )
        if reservation_id == -1:
            return ErrorHandler().bad_request("Product does not exist")

        if reservation_id == -2:
            return ErrorHandler().bad_request("Must Submit an order, not a reservation.")

        if reservation_id == -4:
            return ErrorHandler().bad_request("Not enough resources")

        return (
            self.build_reservation(
                (reservation_id, customer_id, product_id, quantity)
            ),
            201,
        )

    def update_reservation(self, reservation_id, payload):
        reservation_dao = ReservationDAO()
        if not reservation_dao.get_reservation_by_id(reservation_id):
            return ErrorHandler().not_found()

        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            quantity = payload["quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        reservation_id = reservation_dao.update_reservation(
            reservation_id, customer_id, product_id, quantity
        )

        if reservation_id == -1:
            return ErrorHandler().bad_request("Given product does not exist")

        if reservation_id == -2:
            return ErrorHandler().bad_request("Must Submit an order for the new product, not a reservation.")

        if reservation_id == -4:
            return ErrorHandler().bad_request("Not enough resources")

        return (
            self.build_reservation(
                (reservation_id, customer_id, product_id, quantity)
            ),
            200,
        )

    def add_product(self, reservation_id, payload):
        reservation_dao = ReservationDAO()
        if not reservation_dao.get_reservation_by_id(reservation_id):
            return ErrorHandler().not_found()

        try:
            product_id = payload["product_id"]
            quantity = payload["quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        new_quantity = reservation_dao.add_product(reservation_id, product_id, quantity)

        if new_quantity == -1:
            return ErrorHandler().bad_request("Given product does not exist")

        if new_quantity == -2:
            return ErrorHandler().bad_request("Must Submit an order for the new product, not a reservation.")

        if reservation_id == -4:
            return ErrorHandler().bad_request("Not enough resources")

        return self.build_reservation(
            (reservation_id, "same", product_id, new_quantity)
        ), 201

    def delete_reservation(self, reservation_id):
        reservation_dao = ReservationDAO()
        if not reservation_dao.get_reservation_by_id(reservation_id):
            return ErrorHandler().not_found()

        reservation_dao.delete_reservation(reservation_id)
        return jsonify(Deletion="Reservation Deleted"), 200

    def delete_reservations_by_customer_id(self, customer_id):
        reservation_dao = ReservationDAO()
        if not reservation_dao.get_reservations_by_customer_id(customer_id):
            return ErrorHandler().not_found()

        reservation_dao.delete_reservations_by_customer_id(customer_id)
        return jsonify(Deletion="Reservation Deleted"), 200
