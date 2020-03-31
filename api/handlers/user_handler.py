from api.dao.user_dao import UserDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class UserHandler(object):
    def build_user_dict(self, row):
        user_dict = {}
        user_dict["user_id"] = row[0]
        user_dict["username"] = row[1]
        user_dict["password"] = row[2]
        user_dict["phone_number"] = row[3]
        return user_dict

    def get_all_users(self):
        result = UserDAO().get_all_users()
        result_dict = []
        for row in result:
            result_dict.append(self.build_user_dict(row))
        return jsonify(users=result_dict), 200

    def get_user_by_id(self, user_id):
        result = UserDAO().get_user_by_id(user_id)
        if not result:
            return ErrorHandler().not_found()
        else:
            return jsonify(user=[self.build_user_dict(result[0])]), 200

    def insert_user(self, form):
        if form and len(form) == 3:
            username = form["username"]
            password = form["password"]
            phone_number = form["phone_number"]
            if username and password and phone_number:
                result = UserDAO()
                user_id = result.insert(username, password, phone_number)
                result_dict = {}
                result_dict["user_id"] = user_id
                result_dict["username"] = username
                result_dict["password"] = password
                result_dict["phone_id"] = phone_number
                return jsonify(User=result_dict), 201
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

    def updated_user(self, user_id, user):
        if not self.get_user_by_id(user_id):
            return ErrorHandler().not_found()
        try:
            username = user["username"]
            password = user["password"]
            phone_number = user["phone_number"]
        except KeyError:
            ErrorHandler().bad_request()

            if username and password and phone_number:
                user_id = UserDAO().update_user(
                    username,
                    password,
                    phone_number
                )
                return (self.build_user_dict(
                    (
                        username,
                        password,
                        phone_number
                    )
                ), 200)
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()