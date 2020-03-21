from api.dao.product_dao import ProductDAO
from api.dao.location_dao import LocationDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class ProductHandler(object):
    """ Handler for operations involving products. """

    #! Might be unnecessary if dictionary cursor works
    def build_product(self, record):
        """ Returns the dictionary form of a record """

        object_dict = {}
        object_dict["product_id"] = record[0]
        object_dict["product_name"] = record[1]
        object_dict["product_quantity"] = record[2]
        object_dict["product_price"] = record[3]
        object_dict["product_description"] = record[4]
        object_dict["location_id"] = record[5]
        return object_dict

    # General product operations

    def get_all_products(self):
        """ Returns a JSON object containing all product records """

        result = ProductDAO().get_all_products()
        result_dict = []
        for record in result:
            result_dict.append(self.build_product(record))
        return jsonify(products=result_dict), 200

    def get_all_detailed_products(self):
        """ Returns a JSON object containing all products with their additional details """

        result = ProductDAO().get_all_detailed_products()
        return jsonify(detailed_products=result), 200

    def search_products(self, args):
        """ Searches a product by name and returns a JSON object containing it. """

        dao = ProductDAO()
        try:
            product_name = args.get("product_name")
        except KeyError:
            return ErrorHandler().bad_request()

        if product_name:
            result = dao.get_products_by_name(product_name)

        else:
            return ErrorHandler().bad_request()

        result_dict = []
        for record in result:
            result_dict.append(self.build_product(record))
        return jsonify(products=result_dict), 200

    def get_products_by_category(self, args):
        """ Returns a JSON object containing the products in the specified category. """

        try:
            category = args.get("category")
        except KeyError:
            return ErrorHandler().bad_request()

        if category:
            result = ProductDAO().get_products_by_category(category)
            return jsonify(products=result), 200
        else:
            return ErrorHandler().bad_request()

    # Operations by product id

    def get_product_by_id(self, product_id):
        """ Returns a JSON object containing the product with the indicated ID. """

        result = ProductDAO().get_product_by_id(product_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(product=[self.build_product(result[0])]), 200

    def get_detailed_product_by_id(self, product_id):
        """ Returns a JSON object containing the product with the indicated ID. Includes all of the product's details. """

        result = ProductDAO().get_detailed_product_by_id(product_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(product=result), 200

    # Product insertion, update, and deletion

    def insert_product(self, payload):
        """ Adds a product. """

        try:
            product_name = payload["product_name"]
            product_quantity = payload["product_quantity"]
            product_price = payload["product_price"]
            product_description = payload["product_description"]
            latitude = payload["latitude"]
            longitude = payload["longitude"]
        except KeyError:
            return ErrorHandler().bad_request()

        if (
            product_name
            and product_quantity
            and product_price
            and product_description
            and latitude
            and longitude
        ):
            location_id = LocationDAO().insert_location(latitude, longitude)
            product_id = ProductDAO().insert_product(
                product_name,
                product_quantity,
                product_price,
                product_description,
                location_id,
            )
            return (
                self.build_product(
                    (
                        product_id,
                        product_name,
                        product_quantity,
                        product_price,
                        product_description,
                        location_id,
                    )
                ),
                201,
            )
        else:
            return ErrorHandler().bad_request()

    def update_product(self, product_id, payload):
        """ Updates the attributes of the products with the specified id. """

        if not self.get_product_by_id(product_id):
            return ErrorHandler().not_found()
        try:
            product_name = payload["product_name"]
            product_quantity = payload["product_quantity"]
            product_price = payload["product_price"]
            product_description = payload["product_description"]
            latitude = payload["latitude"]
            longitude = payload["longitude"]
        except KeyError:
            return ErrorHandler().bad_request()

        if (
            product_name
            and product_quantity
            and product_price
            and product_description
            and latitude
            and longitude
        ):
            product_id, location_id = ProductDAO().update_product(
                product_id,
                product_name,
                product_quantity,
                product_price,
                product_description,
            )

            LocationDAO().update_location(location_id, latitude, longitude)

            return (
                self.build_product(
                    (
                        product_id,
                        product_name,
                        product_quantity,
                        product_price,
                        product_description,
                        location_id,
                    )
                ),
                200,
            )

        else:
            return ErrorHandler().bad_request()

    def delete_product(self, product_id):
        """ Deletes the product with the specified id. """

        if not self.get_product_by_id(product_id):
            return ErrorHandler().not_found()
        else:
            ProductDAO().delete_product(product_id)
            return jsonify(Deletion="OK"), 200
