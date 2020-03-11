from ds_app.dao.product_dao import ProductDAO
from ds_app.handlers.error_handler import ErrorHandler
from flask import jsonify

class ProductHandler(object):

	def build_product(self, record):
		object_dict = {}
		object_dict['product_id'] = record[0]
		object_dict['product_name'] = record[1]
		object_dict['product_quantity'] = record[2]
		object_dict['description'] = record[3]
		return object_dict
	
	def get_all_products(self):
		result = ProductDAO().get_all_products()
		result_dict = []
		for row in result:
			result_dict.append(self.build_product(row))
		return jsonify(parts=result_dict), 200

	def get_available_products(self):
		result = ProductDAO().get_available_products()
		if not result:
			return ErrorHandler().not_found_error()
		result_dict = []
		for row in result:	
			result_dict.append(self.build_product(row))
		return jsonify(available_parts=result_dict), 200


	def get_all_detailed_products(self):
		return
	
	def get_product_by_id(self, product_id):
		result = ProductDAO().get_product_by_id(product_id)
		if not result:
			return ErrorHandler().not_found_error()
		return jsonify(part=[self.build_product(result[0])])


	def get_detailed_product_by_id(self):
		return

		