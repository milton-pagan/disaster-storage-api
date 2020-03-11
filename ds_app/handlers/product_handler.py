from ds_app.dao.product_dao import ProductDAO
from flask import jsonify

class ProductHandler(object):

	def build_product(self, record):
		object_dict = {}
		object_dict['product_id'] = record[0]
		object_dict['product_name'] = record[1]
		object_dict['description'] = record[2]
		return object_dict



	def get_all_products(self):
		dao = ProductDAO()
		result = dao.get_all_products()
		result_dict = []
		for row in result:
			result_dict.append(self.build_product(row))
		return jsonify(Parts=result_dict)

	def get_all_detailed_products(self):
		return
	
	def get_product_by_id(self, product_id):
		return

		