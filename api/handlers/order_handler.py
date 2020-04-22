from api.dao.order_dao import OrderDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class OrderHandler(object):
    def build_order(self, record):
        ord_dict = {
            "order_id": record[0],
            "customer_id": record[1],
            "product_id": record[2],
            "order_quantity": record[3],
            "order_total": record[4],
        }
        return ord_dict

    def get_all_orders(self):
        results = OrderDAO().get_all_orders()
        res_dict = []
        for order in results:
            res_dict.append(self.build_order(order))
        return jsonify(orders=res_dict)

    def get_order_by_id(self, order_id):
        result = OrderDAO().get_order_by_id(order_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(order=result), 200

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
            order_quantity = payload["order_quantity"]
            order_total = payload["order_total"]
        except KeyError:
            return ErrorHandler().bad_request()

        order_id = OrderDAO().insert_order(
            customer_id, product_id, order_quantity, order_total
        )
        return (
            self.build_order(
                (order_id, customer_id, product_id, order_quantity, order_total)
            ),
            201,
        )

    def update_order(self, order_id, payload):
        if not self.get_order_by_id(order_id):
            return ErrorHandler().not_found()

        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            order_quantity = payload["order_quantity"]
            order_total = payload["order_total"]
        except KeyError:
            return ErrorHandler().bad_request()

        order_id = OrderDAO().update_order(
            customer_id, order_id, product_id, order_quantity, order_total
        )
        return (
            self.build_order(
                (order_id, customer_id, product_id, order_quantity, order_total)
            ),
            200,
        )

    def delete_order(self, order_id):
        if not self.get_order_by_id(order_id):
            return ErrorHandler().not_found()
        else:
            OrderDAO().delete_order(order_id)
            return jsonify(Deletion="Deleted"), 200
