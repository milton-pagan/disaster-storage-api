from flask import make_response, jsonify


class ErrorHandler(object):
    def not_found(self):
        return make_response(jsonify({"Error": "Not found"}), 404)

    def bad_request(self, message="Bad request"):
        return make_response(jsonify({"Error": message}), 400)
