from api.handlers.product_handler import ProductHandler

class RequestDAO(object):

    """ Connection is set here """
    def init(self):
        return

    def get_all_requests(self):
        return [
            {
                "request_id": 1,
                "customer_id": 5,
                "product_id": 30,
                "request_quantity": 5,

            },
            {
                "request_id": 2,
                "customer_id": 7,
                "product_id": 31,
                "request_quantity": 10,
            },
            {
                "request_id": 3,
                "customer_id": 9,
                "product_id": 32,
                "request_quantity": 25,

            },
        ]

    def get_request_by_id(self, request_id):
        return [{
                "request_id": 2,
                "customer_id": 7,
                "product_id": 31,
                "request_quantity": 10
                }]

    def get_requests_by_product_id(self, product_id):
        return [{
                "request_id": 3,
                "customer_id": 9,
                "product_id": 32,
                "request_quantity": 25,
                },
                {
                "request_id": 6,
                "customer_id": 3,
                "product_id": 32,
                "request_quantity": 8,
                }]

    def get_requests_by_customer_id(self, customer_id):
        return [{
                "request_id": 3,
                "customer_id": 9,
                "product_id": 32,
                "request_quantity": 25,
                },
                {
                "request_id": 7,
                "customer_id": 9,
                "product_id": 19,
                "request_quantity": 14,
                }]

    def get_requests_by_keyword(self, keyword):
        """ Search for keyword = Product Name
            Result: Orders joined with Products that match
        """
        return [{
                "request_id": 2,
                "customer_id": 7,
                "product_id": 31,
                "product_name": "ibuprofen",
                "product_price": 4.0,
                "product_description": "painkillers",
                "location_id": 8,
                "request_quantity": 10,
                },
                {
                "request_id": 3,
                "customer_id": 9,
                "product_id": 32,
                "product_name": "Apple Juice",
                "product_price": 2.0,
                "product_description": "Low Sugar",
                "location_id": 8,
                "request_quantity": 5,
                }
                ]

    def insert_request(self, customer_id, product_id, request_quantity):
        request_id = 4
        return request_id

    def update_request(self, request_id, customer_id, product_id, request_quantity):
        request_id = 3
        return request_id

    def delete_request(self, request_id):
        return request_id
