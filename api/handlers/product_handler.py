from api.dao.product_dao import ProductDAO
from api.dao.location_dao import LocationDAO
from api.dao.category_dao import CategoryDAO
from api.handlers.error_handler import ErrorHandler
from flask import jsonify


class ProductHandler(object):
    """ Handler for operations involving products. """

    def build_product(self, record):
        """Returns the dictionary form of a record
        
        Arguments:
            record {tuple} -- A row from product table
        
        Returns:
            dictionary -- Product dictionary
        """

        object_dict = {}
        object_dict["product_id"] = record[0]
        object_dict["product_name"] = record[1]
        object_dict["product_quantity"] = record[2]
        object_dict["product_price"] = record[3]
        object_dict["product_description"] = record[4]
        object_dict["product_category"] = record[5]
        object_dict["location_id"] = record[6]
        return object_dict

    # General product operations

    def get_all_products(self):
        """ Returns a JSON object containing all product records """

        result = ProductDAO().get_all_products()
        return jsonify(products=result), 200

    def search_products(self, args):
        """ Searches a product by keyword in its name and returns a JSON object containing it. """

        dao = ProductDAO()
        try:
            keyword = args.get("keyword")
        except KeyError:
            return ErrorHandler().bad_request()

        if keyword:
            result = dao.get_products_by_keyword(keyword)

            return jsonify(products=result), 200

        else:
            return ErrorHandler().bad_request()

    def get_all_products_by_category(self, category):
        """ Returns a JSON object containing the products in the specified category along with their category specific details. """

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
        return jsonify(product=result), 200

    def get_product_location(self, product_id):
        """Returns the location details of the product with the specified id.
        
        Arguments:
            product_id {int} -- Product Id
        """

        result = ProductDAO().get_product_location(product_id)
        if not result:
            return ErrorHandler().not_found()
        return jsonify(product=result), 200

    def get_detailed_product_by_id(self, product_id):
        """ Returns a JSON object containing the product with the indicated ID. Includes all of the product's details. """
        product_dao = ProductDAO()
        if not product_dao.get_product_by_id(product_id):
            return ErrorHandler().not_found()

        result = product_dao.get_detailed_product_by_id(product_id)

        return jsonify(product=result), 200

    # Product insertion, update, and deletion

    def insert_product(self, payload):
        """ Adds a product and all its information. """
        product_dao = ProductDAO()
        location_dao = LocationDAO()
        category_dao = CategoryDAO()

        try:
            product_name = payload["product_name"]
            product_quantity = payload["product_quantity"]
            product_price = payload["product_price"]
            product_description = payload["product_description"]
            latitude = payload["latitude"]
            longitude = payload["longitude"]
            category = payload["category"]
            category_attributes = payload["category_attributes"]
        except KeyError:
            return ErrorHandler().bad_request()

        # Check that correct attributes for category were passed
        category_response = category_dao.check_category_attributes(
            category, category_attributes
        )
        if category_response:
            return category_response

        location_id = location_dao.insert_location(latitude, longitude)
        product_id = product_dao.insert_product(
            product_name,
            product_quantity,
            product_price,
            product_description,
            category,
            location_id,
        )
        category_id = category_dao.insert_product_category_info(
            category, product_id, category_attributes
        )

        return (
            self.build_product(
                (
                    product_id,
                    product_name,
                    product_quantity,
                    product_price,
                    product_description,
                    category,
                    location_id,
                )
            ),
            201,
        )

    def update_product(self, product_id, payload):
        """Updates the attributes of the products with the specified id
        
        Arguments:
            product_id {int} -- Product ID
            payload {dictionary} -- Holds information to be updated
        
        Returns:
            tuple -- Updated product and/or response
        """

        product_dao = ProductDAO()

        if not product_dao.get_product_by_id(product_id):
            return ErrorHandler().not_found()
        try:
            product_name = payload["product_name"]
            product_quantity = payload["product_quantity"]
            product_price = payload["product_price"]
            product_description = payload["product_description"]
            category = payload["category"]
        except KeyError:
            return ErrorHandler().bad_request()

        location_id = product_dao.update_product(
            product_id,
            product_name,
            product_quantity,
            product_price,
            category,
            product_description,
        )

        return (
            self.build_product(
                (
                    product_id,
                    product_name,
                    product_quantity,
                    product_price,
                    category,
                    product_description,
                    location_id,
                )
            ),
            200,
        )

    def update_product_location(self, product_id, payload):

        product_dao = ProductDAO()
        if not product_dao.get_product_by_id(product_id):
            return ErrorHandler().not_found()

        try:
            latitude = payload["latitude"]
            longitude = payload["longitude"]
        except KeyError:
            return ErrorHandler().bad_request()

        location_id = product_dao.get_product_location_id(product_id)

        LocationDAO().update_location(location_id, latitude, longitude)

        result = {**product_dao.get_product_by_id(product_id), **payload}

        return jsonify(Product=result), 200

    def update_product_category_info(self, product_id, payload):

        product_dao = ProductDAO()
        if not product_dao.get_product_by_id(product_id):
            return ErrorHandler().not_found()

        try:
            category_attributes = payload["category_attributes"]
        except KeyError:
            return ErrorHandler().bad_request()

        category_dao = CategoryDAO()
        category = product_dao.get_product_category(product_id)

        # Check that correct attributes for category were passed
        category_response = category_dao.check_category_attributes(
            category, category_attributes
        )
        if category_response:
            return category_response
        else:
            category_dao.update_product_category_info(
                category, product_id, category_attributes
            )

            result = {
                **product_dao.get_product_by_id(product_id),
                **category_attributes,
            }

            return jsonify(Product=result), 200

    def delete_product(self, product_id):
        """ Deletes the product with the specified id. """

        product_dao = ProductDAO()
        if not product_dao.get_product_by_id(product_id):
            return ErrorHandler().not_found()
        else:

            product_category = product_dao.get_product_category(product_id)
            CategoryDAO().delete_category_info(product_category, product_id)
            location_id = product_dao.delete_product(product_id)
            LocationDAO().delete_location(location_id)

            return jsonify(Deletion="OK"), 200
