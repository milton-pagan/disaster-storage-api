from app.dao.request_dao import RequestDAO
from app.handlers.error_handler import ErrorHandler
from flask import jsonify


class RequestHandler(object):
    def build_request(self, record):
        res_dict = {
            "request_id": record[0],
            "customer_id": record[1],
            "product_id": record[2],
            "request_quantity": record[3],
        }
        return res_dict

    def get_all_requests(self):
        result = RequestDAO().get_all_requests()
        res_dict = []
        for request in result:
            res_dict.append(self.build_request(request))
        return jsonify(requests=res_dict)

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
        try:
            keyword = args.get("keyword")
        except KeyError:
            return ErrorHandler().bad_request()

        if keyword:
            result = RequestDAO().get_requests_by_keyword(keyword)
            return jsonify(orders=result), 200

        return ErrorHandler().bad_request()

    def insert_request(self, payload):
        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            request_quantity = payload["request_quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        request_id = RequestDAO().insert_request(
            customer_id, product_id, request_quantity
        )
        return (
            self.build_request((request_id, customer_id, product_id, request_quantity)),
            201,
        )

    def update_request(self, request_id, payload):
        if not self.get_request_by_id(request_id):
            return ErrorHandler().not_found()

        try:
            customer_id = payload["customer_id"]
            product_id = payload["product_id"]
            request_quantity = payload["request_quantity"]
        except KeyError:
            return ErrorHandler().bad_request()

        request_id = RequestDAO().update_request(
            request_id, customer_id, product_id, request_quantity
        )
        return (
            self.build_request((request_id, customer_id, product_id, request_quantity)),
            200,
        )

    def delete_request(self, request_id):
        if not self.get_request_by_id(request_id):
            return ErrorHandler().not_found()
        else:
            RequestDAO().delete_request(request_id)
            return jsonify(Deletion="Deleted"), 200
