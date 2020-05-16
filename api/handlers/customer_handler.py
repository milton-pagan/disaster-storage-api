from api.dao.customer_dao import CustomerDAO
from api.dao.user_dao import UserDAO
from api.dao.location_dao import LocationDAO
from api.dao.credit_card_dao import CreditCardDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class CustomerHandler(object):

    def build_customer_user(self, record):
        object_dict = {}
        object_dict["customer_id"] = record[0]
        object_dict["customer_first_name"] = record[1]
        object_dict["customer_last_name"] = record[2]
        object_dict["customer_city"] = record[3]
        object_dict["location_id"] = record[4]
        object_dict["user_id"] = record[5]

        return object_dict

    def build_credit_card(self, record):
        object_dict = {}
        object_dict["cc_type"] = record[0]
        object_dict["cc_number"] = record[1]
        object_dict["customer_id"] = record[2]

        return object_dict

    # General Supplier Operations

    def get_all_customers(self):
        result = CustomerDAO().get_all_customer()
        return jsonify(customer=result), 200

    def search_customer(self, customer):
        try:
            customer_city = customer["customer_city"]

        except KeyError:
            ErrorHandler().bad_request()

            if customer_city:
                customers_list = CustomerDAO().get_customers_by_city(customer_city)
                result_list = []
                for row in customers_list:
                    result = self.build_customer(row)
                    result_list.append(result)
                return jsonify(customer=result_list)
            else:
                return ErrorHandler().bad_request()

    # Operations Using Customer ID

    def get_customer_by_id(self, customer_id):
        result = CustomerDAO().get_customer_by_id(customer_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(customer=result), 200

    def get_customer_location_by_id(self, customer_id):
        result = CustomerDAO().get_customer_location_by_id(customer_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(customer=result), 200

    def get_customer_ccard_by_id(self, customer_id):
        result = CustomerDAO().get_customer_ccard_by_id(customer_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(customer=result), 200

    # Operations that return the products names
    # that (order, reserve or request) a specific customer

    def get_product_ordered_by_customer(self, customer_id):
        result = CustomerDAO().get_product_ordered_by_customer(customer_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(customer=result), 200

    def get_product_reserved_by_customer(self, customer_id):
        result = CustomerDAO().get_product_reserved_by_customer(customer_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(customer=result), 200

    def get_product_requested_by_customer(self, customer_id):
        result = CustomerDAO().get_product_requested_by_customer(customer_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(customer=result), 200

    # Supplier insertion, update and deletion

    def insert_customer(self, customer):

        customer_dao = CustomerDAO()
        user_dao = UserDAO()
        location_dao = LocationDAO()
        cc_dao = CreditCardDAO()

        try:
            customer_first_name = customer["customer_first_name"]
            customer_last_name = customer["customer_last_name"]
            customer_city = customer["customer_city"]
            customer_address = customer["customer_address"]
            latitude = customer["latitude"]
            longitude = customer["longitude"]
            username = customer["username"]
            password = customer["password"]
            phone = customer["phone"]

        except KeyError:
            ErrorHandler().bad_request()

        user_id = user_dao.insert_user(username, password, phone)
        location_id = location_dao.insert_location(latitude, longitude)
        customer_id = customer_dao.insert_customer(
                customer_first_name,
                customer_last_name,
                customer_city,
                location_id,
                user_id,
                customer_address,
            )

        return (
            self.build_customer_user(
                (
                    customer_id,
                    customer_first_name,
                    customer_last_name,
                    customer_city,
                    location_id,
                    user_id,
                )
            ),
            201,
        )

    def insert_credit_card_by_customer_id(self, customer_id, card):
        credit_card_dao = CreditCardDAO()

        try:
            cc_type = card["cc_type"]
            cc_number = card["cc_number"]

        except KeyError:
            ErrorHandler().bad_request()

        credit_id = credit_card_dao.insert_credit_card(cc_type, cc_number, customer_id)

        return (
            self.build_credit_card(
                (
                    cc_type,
                    cc_number,
                    customer_id
                )
            ),
            201,
        )

    def update_customer(self, customer_id, customer):
        if not self.get_customer_by_id(customer_id):
            return ErrorHandler().not_found()

        try:
            customer_first_name = customer["customer_first_name"]
            customer_last_name = customer["customer_last_name"]
            customer_city = customer["customer_city"]
            latitude = customer["latitude"]
            longitude = customer["longitude"]
            cc_id = customer["cc_id"]
            cc_type = customer["cc_type"]
            cc_number = customer["cc_number"]

        except KeyError:
            ErrorHandler().bad_request()

            customer_id, location_id = CustomerDAO().update_customer(customer_first_name, customer_last_name, customer_city,)
            LocationDAO().update_location(location_id, latitude, longitude)
            CreditCardDAO().update_credit_card(
                    cc_id, cc_number, cc_type, customer_id
                )

            return (
                    self.build_customer_user(
                        (
                            customer_id,
                            customer_first_name,
                            customer_last_name,
                            customer_city,
                            location_id,
                        )
                    ),
                    200,
                )


    def delete_customer(self, customer_id):
        if not self.get_customer_by_id(customer_id):
            return ErrorHandler().not_found()
        else:
            CustomerDAO().delete_customer(customer_id)
            return jsonify(Deletion="OK"), 200
