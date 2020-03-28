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
        result = SupplierDAO()

