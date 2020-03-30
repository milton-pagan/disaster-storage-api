from api.dao.order_dao import OrderDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify

"""
order_id
order_quantity
order_total

"""
class OrderHandler(object):

    def build_order(self, record):
        ord_dict = {"order_id": record[0],
                    "product_id": record[1],
                    "order_quantity": record[1],
                    "order_total": record[2]}
        return ord_dict

    def get_all_orders(self):
        results = OrderDAO().get_all_orders()
        res_dict = []
        for order in results:
            res_dict.append(self.build_order(order))
        return jsonify(orders=res_dict)

    def get_all_detailed_orders(self):
        results = OrderDAO().get_all_detailed_orders()
        return jsonify(detailed_orders=results)

    def get_order_by_id(self, order_id):
        result = OrderDAO().get_order_by_id(order_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(order=result), 200

    def get_detailed_order_by_id(self, order_id):
        result = OrderDAO().get_detailed_order_by_id(order_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(order=result), 200

    def get_orders_by_product(self, product_id):
        results = OrderDAO().get_orders_by_product(product_id)
        if not results:
            return ErrorHandler().not_found()
        return jsonify(orders=results), 200

    def get_detailed_orders_by_product(self, product_id):
        results = OrderDAO().get_detailed_orders_by_product(product_id)
        if not results:
            return ErrorHandler().not_found()

        res_dict = []
        for order in results:
            res_dict.append(self.build_order(order))
        return jsonify(orders=res_dict)


    def insert_order(self, payload):
        try:
            product_id = payload["product_id"]
            order_quantity = payload["order_quantity"]
            order_total = payload["order_total"]
        except KeyError:
            return ErrorHandler().bad_request()

        if product_id and order_quantity and order_total:
            order_id = OrderDAO().insert_order(product_id, order_quantity, order_total)

            return (self.build_order((order_id, product_id, order_quantity, order_total))), 201

        else:
            return ErrorHandler().bad_request()

    def update_order(self, order_id, payload):
        if not self.get_order_by_id(order_id):
            return ErrorHandler().not_found()

        try:
            product_id = payload["product_id"]
            order_quantity = payload["order_quantity"]
            order_total = payload["order_total"]
        except KeyError:
            return ErrorHandler().bad_request()

        if product_id and order_quantity and order_total:
            order_id = OrderDAO().update_order(order_id, product_id, order_quantity, order_total)

            return (self.build_order((order_id, product_id, order_quantity,order_total))), 200

    def delete_order(self, order_id):
        if not self.get_order_by_id(order_id):
            return ErrorHandler().not_found()

        else:
            OrderDAO().delete_order(order_id)
            return jsonify(Deletion="Deleted"), 200