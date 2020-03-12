from ds_app.dao.product_dao import ProductDAO
from ds_app.handlers.error_handler import ErrorHandler
from flask import jsonify


class ProductHandler(object):
    def build_product(self, record):
        object_dict = {}
        object_dict["product_id"] = record[0]
        object_dict["product_name"] = record[1]
        object_dict["product_quantity"] = record[2]
        object_dict["product_price"] = record[3]
        object_dict["product_description"] = record[4]
        object_dict["location_id"] = record[5]
        return object_dict

    def get_all_products(self):
        result = ProductDAO().get_all_products()
        result_dict = []
        for record in result:
            result_dict.append(self.build_product(record))
        return jsonify(parts=result_dict), 200

    def get_all_detailed_products(self):
        result = ProductDAO().get_all_detailed_products()
        return jsonify(detailed_parts=result), 200

    # DEPRECATED
    def get_available_products(self):
        result = ProductDAO().get_available_products()
        result_dict = []
        for record in result:
            result_dict.append(self.build_product(record))
        return jsonify(available_parts=result_dict), 200

    def get_product_by_id(self, product_id):
        result = ProductDAO().get_product_by_id(product_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(part=[self.build_product(result[0])])

    def get_detailed_product_by_id(self, product_id):
        result = ProductDAO().get_detailed_product_by_id(product_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(part=result)

    def search_product(self, args):
        dao = ProductDAO()

        product_name = args.get("product_name")
        product_price = args.get("product_price")
        method = args.get("method")

        if product_name and not product_price:
            result = dao.get_products_by_name(product_name)

        elif product_price and not product_name and method == ">":
            result = dao.get_products_by_greater_price(product_price)

        elif product_price and not product_name and method == "<":
            result = dao.get_products_by_smaller_price(product_price)

        elif product_name and product_price and method == ">":
            result = dao.get_products_by_name_and_greater_price(
                product_name, product_price
            )

        elif product_name and product_price and method == "<":
            result = dao.get_products_by_name_and_smaller_price(
                product_name, product_price
            )

        else:
            return ErrorHandler().bad_request()

        result_dict = []
        for record in result:
            result_dict.append(self.build_product(record))
        return jsonify(parts=result_dict), 200

    # DEPRECATED
    def search_available(self, args):
        return
