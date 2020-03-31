import psycopg2

class SupplierDAO(object):

    def init(self):
        return

    # General Supplier Operations

    def get_all_suppliers(self):
        return [
            (1, "Sam's", "San Juan", 4),
            (2, "Pep Boys", "Mayaguez", 5),
            (3, "Wallgreens", "Bayamon", 6)
        ]

    def get_suppliers_by_city(self, supplier_city):
        return [(3, "Wallgreens", "Bayamon", 3)]

    # Operations using Supplier Id

    def get_supplier_by_id(self, supplier_id):
        return [(2, "Pep Boys", "Mayaguez", 2)]

    def get_products_by_supplier_id(self, supplier_id):
        return [(1, "water bottle", 100, 0.0, "bottle of water", 1),
            (2, "bouillon sausages", 50, 0.0, "8 count can", 2)]

    def insert_supplier(
            self,
            supplier_name,
            supplier_city,
            location_id,
            user_id
    ):
        supplier_id = 10
        return supplier_id

    def update_supplier(
            self,
            supplier_id,
            supplier_name,
            supplier_city,
            location_id
    ):
        return supplier_id, location_id

    def delete_supplier(self, supplier_id):
        return supplier_id