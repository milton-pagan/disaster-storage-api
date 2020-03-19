from api.dao.customer_dao import CustomerDAO
from flask import jsonify


class CustomerHandler(object):
    def build_customer_dict(self, record):
        customer_dict = {}
        customer_dict["customer_id"] = record[0]
        customer_dict["customer_name"] = record[1]
        customer_dict["customer_city"] = record[2]
        customer_dict["location_id"] = record[3]
        return customer_dict

    def insert_customer(self, payload):
        return
