from api.dao.customer_dao import CustomerDAO
from api.dao.user_dao import UserDAO
from api.dao.location_dao import LocationDAO
from api.dao.credit_card_dao import CreditCardDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class CustomerHandler(object):
 
    def build_customer(self, record):
        object_dict = {}
        object_dict["customer_id"] = record[0]
        object_dict["customer_first_name"] = record[1]
        object_dict["supplier_last_name"] = record[2]
        object_dict["location_id"] = record[3]
        return object_dict

    def build_customer_user(self, record):
        object_dict = {}
        object_dict["customer_id"] = record[0]
        object_dict["customer_first_name"] = record[1]
        object_dict["supplier_last_name"] = record[2]
        object_dict["location_id"] = record[3]
        object_dict["cc_id"] = record[4]
        object_dict["user_id"] = record[5]

        return object_dict

    #General Supplier Operations

    def get_all_customers(self):
        result = CustomerDAO().get_all_customer()
        result_dict = []
        for record in result:
            result_dict.append(self.build_customer(record))
        return jsonify(customer=result_dict), 200

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

    def get_customer_by_id(self, customer_id):
        result = CustomerDAO().get_customer_by_id(customer_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(customer=[self.build_customer(result[0])]), 200

    # Supplier insertion, update and deletion

    def insert_customer(self, customer):
        try:
            customer_first_name = customer["customer_first_name"]
            customer_last_name = customer["customer_last_name"]
            customer_city = customer["customer_city"]
            latitude = customer["latitude"]
            longitude = customer["longitude"]
            customer_username = customer["customer_username"]
            customer_password = customer["customer_password"]
            customer_phone = customer["customer_phone"]
            customer_cc_type = customer["cc_type"]
            customer_cc_number = customer["cc_number"]
            customer_cc_exp = customer["cc_exp"]
            customer_cc_sec_code = customer["cc_sec_code"]

        except KeyError:
            ErrorHandler().bad_request()

            if (
                customer_first_name and customer_last_name and
                customer_city and latitude and longitude and
                customer_username and customer_password and
                customer_phone and customer_cc_type and customer_cc_number and
                customer_cc_exp and customer_cc_sec_code
            ):
                location_id = LocationDAO().insert_location(latitude, longitude)
                user_id = UserDAO().insert_user(
                    customer_username,
                    customer_password,
                    customer_phone
                )
                customer_id = CustomerDAO().insert_customer(
                    customer_first_name,
                    customer_last_name,
                    customer_city,
                    location_id,
                    user_id
                )
                cc_id = CreditCardDAO().insert_credit_card(
                    customer_cc_type,
                    customer_cc_number,
                    customer_cc_exp,
                    customer_cc_sec_code
                )
                return (self.build_customer_user(
                    (
                        customer_id,
                        customer_first_name,
                        customer_last_name,
                        customer_city,
                        location_id,
                        cc_id,
                        user_id
                    )
                ), 201)
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

    def update_customer(self, customer_id, customer):
        if not self.get_customer_by_id(customer_id):
            return ErrorHandler().not_found()

        try:
            customer_first_name = customer["customer_first_name"]
            customer_last_name = customer["customer_last_name"]
            customer_city = customer["customer_city"]
            latitude = customer["latitude"]
            longitude = customer["longitude"]
        except KeyError:
            ErrorHandler().bad_request()

            if customer_first_name and customer_last_name and customer_city and latitude and longitude:
                customer_id, location_id = CustomerDAO().update_customer(
                    customer_id,
                    customer_first_name,
                    customer_last_name,
                    customer_city,
                )
                LocationDAO().update_location(location_id, latitude, longitude)

                return (self.build_customer(
                    (
                        customer_id,
                        customer_first_name,
                        customer_last_name,
                        customer_city,
                        location_id
                    )
                ), 200)
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

    def delete_customer(self, customer_id):
        if not self.get_customer_by_id(customer_id):
            return ErrorHandler().not_found()
        else:
            CustomerDAO().delete_customer(customer_id)
            return jsonify(Deletion="OK"), 200
