import psycopg2


class ProductDAO(object):
    # Connection to backend is set up here
    def init(self):
        return

    # Returns available products (in stock)
    def get_all_products(self):
        return [
            (1, "water bottle", 100, 0.0, "bottle of water", 1),
            (2, "bouillon sausages", 50, 0.0, "8 count can", 2),
            (3, "ibuprofen", 20, 4.0, "generic", 1),
        ]

    def get_all_detailed_products(self):
        # USE A DICTIONARY CURSOR HERE
        # Must join with categories
        return [
            {
                "product_id": 1,
                "product_name": "water bottle",
                "product_quantity": 100,
                "product_price": 0.0,
                "product_description": "bottle of water",
                "location_id": 1,
                "exp_date": "2020-06-22",
                "volume_ml": 500,
                "location_latitude": 18.20985,
                "location_longitude": -67.13918,
            },
            {
                "product_id": 2,
                "product_name": "bouillon sausages",
                "product_quantity": 50,
                "product_price": 0.0,
                "product_description": "8 count",
                "location_id": 2,
                "exp_date": "2020-06-22",
                "weight_g": 80.0,
                "location_latitude": 18.20985,
                "location_longitude": -67.13918,
            },
            {
                "product_id": 3,
                "product_name": "ibuprofen",
                "product_quantity": 20,
                "product_price": 4.0,
                "product_description": "painkillers",
                "location_id": 1,
                "type": "pills",
                "exp_date": "2020-06-22",
                "location_latitude": 18.20985,
                "location_longitude": -67.13918,
            },
        ]

    def get_available_products(self):
        return [
            (1, "water bottle", 100, 0.0, "bottle of water", 1),
            (3, "ibuprofen", 20, 4.0, "generic", 1),
        ]

    def get_product_by_id(self, product_id):
        # Query by id
        return [(1, "water bottle", 100, 0.0, "bottle of water", 1)]

    def get_detailed_product_by_id(self, product_id):
        return [
            {
                "product_id": 1,
                "product_name": "water bottle",
                "product_quantity": 100,
                "product_price": 0.0,
                "product_description": "bottle of water",
                "location_id": 1,
                "exp_date": "2020-06-22",
                "volume_ml": 500,
                "location_latitude": 18.20985,
                "location_longitude": -67.13918,
            }
        ]

    def get_available_products_by_name(self, product_name):
        # Query by name and quantity > 0, sort by name
        return [(3, "ibuprofen", 20, 4.0, "generic", 1)]

    def insert_product(self, product_name, product_quantity, product_price, product_description, location_id):
        product_id = 3
        return product_id
