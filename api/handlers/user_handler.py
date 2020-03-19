from api.dao.user_dao import UserDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class UserHandler(object):
    def build_user_dict(self, record):
        user_dict = {}
        user_dict["user_id"] = record[0]
        user_dict["username"] = record[1]
        user_dict["password"] = record[2]
        user_dict["phone_number"] = record[3]
        return user_dict

    def get_all_users(self):
        result = UserDAO().get_all_users()
        result_dict = []
        for record in result:
            result_dict.append(self.build_user_dict(record))
        return jsonify(users=result_dict), 200

    def get_user_by_id(self, user_id):
        result = UserDAO().get_user_by_id(user_id)
        if not result:
            return ErrorHandler().not_found()
        else:
            return jsonify(user=[self.build_user_dict(result[0])]), 200

    # TODO
    def update_user(self, user_id, payload):
        return

    # TODO
    def delete_user(self, user_id):
        return

    def insert_user(self, payload):
        if payload and len(payload) == 3:
            username = payload["username"]
            password = payload["password"]
            phone_number = payload["phone_number"]
            if username and password and phone_number:
                dao = UserDAO()
                user_id = dao.insert_user(username, password, phone_number)
                result_dict = {}
                result_dict["user_id"] = user_id
                result_dict["username"] = username
                result_dict["password"] = password
                result_dict["phone_number"] = phone_number
                return jsonify(User=result_dict), 201
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

