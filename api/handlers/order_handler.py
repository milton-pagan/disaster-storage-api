from api.dao.order_dao import OrderDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class OrderHandler(object):
    def build_order(self, record):
        ord_dict = {
            "order_id": record[0],
            "customer_id": record[1],
            "product_id": record[2],
            "quantity": record[3],
            "order_total": record[4],
        }
        return ord_dict

    def get_all_orders(self):
        results = OrderDAO().get_all_orders()
        return jsonify(orders=results)

    def get_order_by_id(self, order_id):
        results = OrderDAO().get_order_by_id(order_id)
        if not results:
            return ErrorHandler().not_found()
        return jsonify(orders=results), 200

    def get_orders_by_product_id(self, product_id):
        results = OrderDAO().get_orders_by_product_id(product_id)
        if not results:
            return ErrorHandler().not_found()
        return jsonify(orders=results), 200

    def get_orders_by_customer_id(self, customer_id):
        results = OrderDAO().get_orders_by_customer_id(customer_id)
        if not results:
            return ErrorHandler().not_found()
        return jsonify(orders=results), 200

    def insert_order(self, payload):
        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            quantity = payload["quantity"]
            order_total = payload["order_total"]
        except KeyError:
            return ErrorHandler().bad_request()

        order_id = OrderDAO().insert_order(
            customer_id, product_id, quantity, order_total
        )
        if order_id == -1:
            return ErrorHandler().bad_request("Customer without credit card")

        if order_id == -2:
            return ErrorHandler().bad_request("Product does not exist")

        if order_id == -3:
            return ErrorHandler().bad_request("Must Submit a reservation, not a order.")

        return (
            self.build_order(
                (order_id, customer_id, product_id, quantity, order_total)
            ),
            201,
        )

    def update_order(self, order_id, payload):
        order_dao = OrderDAO()
        if not order_dao.get_order_by_id(order_id):
            return ErrorHandler().not_found()

        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            quantity = payload["quantity"]
            order_total = payload["order_total"]
        except KeyError:
            return ErrorHandler().bad_request()

        order_id = order_dao.update_order(
            customer_id, order_id, product_id, quantity, order_total
        )
        if order_id == -1:
            return ErrorHandler().bad_request("New customer without credit card")

        if order_id == -2:
            return ErrorHandler().bad_request("Product does not exist")

        if order_id == -3:
            return ErrorHandler().bad_request("Must Submit a reservation for the new product, not a order.")

        return (
            self.build_order(
                (order_id, customer_id, product_id, quantity, order_total)
            ),
            200,
        )

    def add_product(self, order_id, payload):
        order_dao = OrderDAO()
        if not order_dao.get_order_by_id(order_id):
            return ErrorHandler().not_found()

        try:
            product_id = payload["product_id"]
            quantity = payload["quantity"]
            total = payload["total"]
        except KeyError:
            return ErrorHandler().bad_request()

        order_total = order_dao.add_product(order_id, product_id, quantity, total)

        if order_id == -2:
            return ErrorHandler().bad_request("Product does not exist")

        if order_id == -3:
            return ErrorHandler().bad_request("Must Submit a reservation for the new product, not a order.")

        return self.build_order(
            (order_id, "same", product_id, quantity, order_total)
        ), 201

    def delete_order(self, order_id):
        order_dao = OrderDAO()
        if not order_dao.get_order_by_id(order_id):
            return ErrorHandler().not_found()

        order_dao.delete_order(order_id)
        return jsonify(Deletion="Order deleted"), 200

    def delete_order_by_customer_id(self, customer_id):
        order_dao = OrderDAO()
        if not order_dao.get_orders_by_customer_id(customer_id):
            return ErrorHandler().not_found()

        order_dao.delete_order_by_customer_id(customer_id)
        return jsonify(Deletion="Orders deleted"), 200
