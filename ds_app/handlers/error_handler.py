from flask import make_response, jsonify

class ErrorHandler(object):

    def not_found_error(self):
        return make_response(jsonify({'Error': 'Not found'}), 404)