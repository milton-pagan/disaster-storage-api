from api.dao.admin_dao import AdminDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class AdminHandler(object):
    def build_admin_dict(self, row):
        admin_dict = {}
        admin_dict["admin_id"] = row[0]
        admin_dict["admin_name"] = row[1]
        return admin_dict

    def get_all_admins(self):
        result = AdminDAO().get_all_admins()
        result_dict = []
        for row in result:
            result_dict.append(self.build_admin_dict(row))
        return jsonify(admin=result_dict), 200

    def get_admin_by_id(self, user_id):
        result = AdminDAO().get_admin_by_id(user_id)
        if not result:
            return ErrorHandler().not_found()
        else:
            return jsonify(admin=[self.build_admin_dict(result[0])]), 200

    def insert_admin(self, admin):
        try:
            admin_name = admin["admin_name"]

        except KeyError:
            ErrorHandler().bad_request()

            if admin_name:
                admin_id = AdminDAO().insert_admin(admin_name)
                return (self.build_admin_dict(admin_id, admin_name)), 201

            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

    def update_admin(self, admin_id, admin):
        if not self.get_admin_by_id(admin_id):
            return ErrorHandler().not_found()

        try:
            admin_name = admin["admin_name"]

        except KeyError:
            ErrorHandler().bad_request()

            if admin_name:
                AdminDAO().update_admin(admin_id, admin_name)

                return (self.build_admin_dict((admin_id, admin_name)), 200)
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

    def delete_admin(self, admin_id):
        if not self.get_admin_by_id(admin_id):
            return ErrorHandler().not_found()
        else:
            AdminDAO().delete_admin(admin_id)
            return jsonify(Deletion="OK"), 200
