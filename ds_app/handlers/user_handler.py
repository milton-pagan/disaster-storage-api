from ds_app.dao.user_dao import UserDAO
from ds_app.handlers.error_handler import ErrorHandler
from flask import jsonify



class UserHandler(object):

    def build_user_dict(self, row):
        user_dict = {}
        user_dict['user_id'] = row[0]
        user_dict['username'] = row[1]
        user_dict['password'] = row[2]
        user_dict['phone'] = row[3]
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
            return ErrorHandler().not_found_error()
        else:
            return jsonify(user=[self.build_user_dict(result[0])])



