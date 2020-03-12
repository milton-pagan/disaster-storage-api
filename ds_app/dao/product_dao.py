import psycopg2


class ProductDAO(object):
	# Connection to backend is set up here
	def init(self):
		return

	def get_all_products(self):
		return [(1, 'water bottle', 100, '7 fl. oz'), (2, 'bouillon sausages', 0, '8 count can'), (3, 'ibuprofen', 20, 'generic')]

	def get_all_detailed_products(self):
		return

	# Returns available products (in stock)
	def get_available_products(self):
		return [(1, 'water bottle', 100, '7 fl. oz'), (3, 'ibuprofen', 20, 'generic')]

	def get_product_by_id(self, product_id):
		# Search by id
		return [(1, 'water bottle', 100, '7 fl. oz')]
