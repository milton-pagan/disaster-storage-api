from api.dao.supplier_dao import SupplierDAO
from api.dao.location_dao import LocationDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify

class SupplierHandler(object):

    def build_supplier(self, record):
        object_dict = {}
        object_dict["supplier_id"] = record[0]
        object_dict["supplier_name"] = record[1]
        object_dict["supplier_city"] = record[2]
        object_dict["location_id"] = record [3]
        return object_dict

    #General Supplier Operations

    def get_all_suppliers(self):
        result = SupplierDAO().get_all_suppliers()
        result_dict = []
        for record in result:
            result_dict.append(self.build_supplier(record))
        return jsonify(supplier=result_dict), 200

    def search_suppliers(self, args):
        if len(args) > 1:
            return ErrorHandler().bad_request()
        else:
            supplier_city = args.get("city")
            if supplier_city:
                supplier_list = SupplierDAO().get_suppliers_by_city(supplier_city)
                result_list = []
                for row in supplier_list:
                    result = self.build_supplier(row)
                    result_list.append(row)
                return jsonify(suppliers=result_list)
            else:
                return ErrorHandler().bad_request()

    def get_supplier_by_id(self, supplier_id):
        result = SupplierDAO().get_supplier_by_id(supplier_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(supplier=[self.build_supplier(result[0])]), 200

    # Supplier insertion, update and deletion

    def insert_supplier(self, supplier):
        if supplier and len(supplier) == 4:
            supplier_name = supplier["supplier_name"]
            supplier_city = supplier["supplier_city"]
            latitude = supplier["latitude"]
            longitude = supplier["longitude"]

            if supplier_name and supplier_city and latitude and longitude:
                location_id = LocationDAO().insert_location(latitude, longitude)
                supplier_id = SupplierDAO().insert_supplier(supplier_name, supplier_city, location_id)

                return (self.build_supplier(
                    (
                        supplier_id,
                        supplier_name,
                        supplier_city,
                        location_id
                    )
                ), 201)
            else:
                return ErrorHandler().bad_request()
        else:
            return ErrorHandler().bad_request()

    def update_supplier(self, supplier_id, supplier):
        if not self.get_supplier_by_id(supplier_id):
            return ErrorHandler().not_found()

        if supplier and len(supplier) == 3:
            supplier_name = supplier["supplier_name"]
            supplier_city = supplier["supplier_city"]
            latitude = supplier["latitude"]
            longitude = supplier["longitude"]

            if supplier_name and supplier_city and latitude and longitude:
                supplier_id, location_id = SupplierDAO().update_supplier(
                    supplier_id,
                    supplier_name,
                    supplier_city,
                )
                LocationDAO().update_location(location_id, latitude, longitude)

                return (self.build_supplier(
                    (
                        supplier_id,
                        supplier_name,
                        supplier_city,
                        location_id
                    )
                ), 200)
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
