from api.dao.customer_dao import CustomerDAO
from api.dao.location_dao import LocationDAO
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

    #General Supplier Operations

    def get_all_customers(self):
        result = CustomerDAO().get_all_customer()
        result_dict = []
        for record in result:
            result_dict.append(self.build_customer(record))
        return jsonify(customer=result_dict), 200

    def search_customer(self, args):
        if len(args) > 1:
            return ErrorHandler().bad_request()
        else:
            customer_city = args.get("city")
            if customer_city:
                customers_list = CustomerDAO().get_customers_by_city(customer_city)
                result_list = []
                for row in customers_list:
                    result = self.build_customer(row)
                    result_list.append(row)
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
        if customer and len(customer) == 5:
            customer_first_name = customer["customer_first_name"]
            customer_last_name = customer["customer_last_name"]
            customer_city = customer["customer_city"]
            latitude = customer["latitude"]
            longitude = customer["longitude"]

            if customer_first_name and customer_last_name and customer_city and latitude and longitude:
                location_id = LocationDAO().insert_location(latitude, longitude)
                customer_id = CustomerDAO().insert_customer(
                    customer_first_name,
                    customer_last_name,
                    customer_city,
                    location_id
                )

                return (self.build_customer(
                    (
                        customer_id,
                        customer_first_name,
                        customer_last_name,
                        customer_city,
                        location_id
                    )
                ), 201)
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

    def update_customer(self, customer_id, customer):
        if not self.get_customer_by_id(customer_id):
            return ErrorHandler().not_found()

        if customer and len(customer) == 5:
            customer_first_name = customer["customer_first_name"]
            customer_last_name = customer["customer_last_name"]
            customer_city = customer["customer_city"]
            latitude = customer["latitude"]
            longitude = customer["longitude"]

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
