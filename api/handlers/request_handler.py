from api.dao.request_dao import RequestDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class RequestHandler(object):
    def build_request(self, record):
        res_dict = {
            "request_id": record[0],
            "customer_id": record[1],
            "product_id": record[2],
            "quantity": record[3],
        }
        return res_dict

    def get_all_requests(self):
        results = RequestDAO().get_all_requests()
        return jsonify(requests=results)

    def get_request_by_id(self, request_id):
        result = RequestDAO().get_request_by_id(request_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(request=result), 200

    def get_requests_by_product_id(self, product_id):
        results = RequestDAO().get_requests_by_product_id(product_id)
        if not results:
            return ErrorHandler().not_found()
        return jsonify(requests=results), 200

    def get_requests_by_customer_id(self, customer_id):
        results = RequestDAO().get_requests_by_customer_id(customer_id)
        if not results:
            return ErrorHandler().not_found()
        return jsonify(requests=results), 200

    def search_requests(self, args):
        request_dao = RequestDAO()
        try:
            keyword = args.get("keyword")
        except KeyError:
            return ErrorHandler().bad_request()

        if keyword:
            result = request_dao.get_requests_by_keyword(keyword)
            return jsonify(orders=result), 200

        return ErrorHandler().bad_request()

    def insert_request(self, payload):
        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            quantity = payload["quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        request_id = RequestDAO().insert_request(
            customer_id, product_id, quantity
        )
        if request_id == -1:
            return ErrorHandler().bad_request("Product does not exist")
        return (
            self.build_request((request_id, customer_id, product_id, quantity)),
            201,
        )

    def update_request(self, request_id, payload):
        request_dao = RequestDAO()
        if not request_dao.get_request_by_id(request_id):
            return ErrorHandler().not_found()

        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            quantity = payload["quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        request_id = RequestDAO().update_request(
            request_id, customer_id, product_id, quantity
        )

        if request_id == -1:
            return ErrorHandler().bad_request("Given product does not exist")

        return (
            self.build_request((request_id, customer_id, product_id, quantity)),
            200,
        )

    def add_product(self, request_id, payload):
        request_dao = RequestDAO()
        if not request_dao.get_request_by_id(request_id):
            return ErrorHandler().not_found()

        try:
            product_id = payload["product_id"]
            quantity = payload["quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        new_quantity = request_dao.add_product(request_id, product_id, quantity)

        if new_quantity == -1:
            return ErrorHandler().bad_request("Given product does not exist")

        return self.build_request(
            (request_id, "same", product_id, new_quantity)
        ), 201

    def delete_request(self, request_id):
        request_dao = RequestDAO()
        if not request_dao.get_request_by_id(request_id):
            return ErrorHandler().not_found()

        request_dao.delete_request(request_id)
        return jsonify(Deletion="Request Deleted"), 200

    def delete_requests_by_customer_id(self, customer_id):
        request_dao = RequestDAO()
        if not request_dao.get_requests_by_customer_id(customer_id):
            return ErrorHandler().not_found()

        request_dao.delete_requests_by_customer_id(customer_id)
        return jsonify(Deletion="Reservations Deleted"), 200
