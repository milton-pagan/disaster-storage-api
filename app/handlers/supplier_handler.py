from app.dao.supplier_dao import SupplierDAO
from app.dao.user_dao import UserDAO
from app.dao.location_dao import LocationDAO
from app.handlers.error_handler import ErrorHandler
from flask import jsonify


class SupplierHandler(object):
    def build_supplier(self, record):
        object_dict = {}
        object_dict["supplier_id"] = record[0]
        object_dict["supplier_name"] = record[1]
        object_dict["supplier_city"] = record[2]
        object_dict["location_id"] = record[3]
        return object_dict

    def build_supplier_user(self, record):
        object_dict = {}
        object_dict["supplier_id"] = record[0]
        object_dict["supplier_name"] = record[1]
        object_dict["supplier_city"] = record[2]
        object_dict["location_id"] = record[3]
        object_dict["user_id"] = record[4]
        return object_dict

    def build_product(self, record):
        object_dict = {}
        object_dict["product_id"] = record[0]
        object_dict["product_name"] = record[1]
        object_dict["product_quantity"] = record[2]
        object_dict["product_price"] = record[3]
        object_dict["product_description"] = record[4]
        object_dict["location_id"] = record[5]
        return object_dict

    # General Supplier Operations

    def get_all_suppliers(self):
        result = SupplierDAO().get_all_suppliers()
        result_dict = []
        for record in result:
            result_dict.append(self.build_supplier(record))
        return jsonify(supplier=result_dict), 200

    def search_suppliers(self, supplier):
        try:
            supplier_city = supplier["customer_city"]
        except KeyError:
            ErrorHandler().bad_request()

            if supplier_city:
                supplier_list = SupplierDAO().get_suppliers_by_city(supplier_city)
                result_list = []
                for row in supplier_list:
                    result = self.build_supplier(row)
                    result_list.append(result)
                return jsonify(suppliers=result_list)
            else:
                return ErrorHandler().bad_request()

    def get_supplier_by_id(self, supplier_id):
        result = SupplierDAO().get_supplier_by_id(supplier_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(supplier=[self.build_supplier(result[0])]), 200

    def get_products_by_supplier_id(self, supplier_id):
        if not SupplierDAO().get_products_by_supplier_id(supplier_id):
            return ErrorHandler().not_found()

        parts_list = SupplierDAO().get_products_by_supplier_id(supplier_id)
        result_list = []
        for row in parts_list:
            result = self.build_product(row)
            result_list.append(result)
        return jsonify(ProductsSupplier=result_list)

    # Supplier insertion, update and deletion

    def insert_supplier(self, supplier):
        try:
            supplier_name = supplier["customer_first_name"]
            supplier_city = supplier["customer_city"]
            latitude = supplier["latitude"]
            longitude = supplier["longitude"]
            supplier_username = supplier["supplier_username"]
            supplier_password = supplier["supplier_password"]
            supplier_phone = supplier["supplier_phone"]

        except KeyError:
            ErrorHandler().bad_request()

            if (
                supplier_name
                and supplier_city
                and latitude
                and longitude
                and supplier_username
                and supplier_password
                and supplier_phone
            ):

                location_id = LocationDAO().insert_location(latitude, longitude)
                supplier_id = SupplierDAO().insert_supplier(
                    supplier_name, supplier_city, location_id
                )
                user_id = UserDAO().insert_user(
                    supplier_username, supplier_password, supplier_phone
                )

                return (
                    self.build_supplier_user(
                        (
                            supplier_id,
                            supplier_name,
                            supplier_city,
                            location_id,
                            user_id,
                        )
                    ),
                    201,
                )
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

    def update_supplier(self, supplier_id, supplier):
        if not self.get_supplier_by_id(supplier_id):
            return ErrorHandler().not_found()

        try:
            supplier_name = supplier["customer_first_name"]
            supplier_city = supplier["customer_city"]
            latitude = supplier["latitude"]
            longitude = supplier["longitude"]
        except KeyError:
            ErrorHandler().bad_request()

            if supplier_name and supplier_city and latitude and longitude:
                supplier_id, location_id = SupplierDAO().update_supplier(
                    supplier_id, supplier_name, supplier_city,
                )
                LocationDAO().update_location(location_id, latitude, longitude)

                return (
                    self.build_supplier(
                        (supplier_id, supplier_name, supplier_city, location_id)
                    ),
                    200,
                )
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

    def delete_supplier(self, supplier_id):
        if not self.get_supplier_by_id(supplier_id):
            return ErrorHandler().not_found()
        else:
            SupplierDAO().delete_supplier(supplier_id)
            return jsonify(Deletion="OK"), 200
