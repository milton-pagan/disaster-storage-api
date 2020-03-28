import psycopg2

class SupplierDAO(object):

    def init(self):
        return

    #General Supplier Operations

    def get_all_suppliers(self):
        return [
            (1, "Sam's", "San Juan", 1),
            (2, "Pep Boys", "Mayaguez", 2),
            (3, "Wallgreens", "Bayamon", 3)
        ]

    def get_supplier_by_city(self, supplier_city):
        return [(3, "Wallgreens", "Bayamon", 3)]

    #Operations using Supplier Id

    def get_supplier_by_id(self):
        return [(2, "Pep Boys", "Mayaguez", 2)]


    def insert_supplier(
            self,
            supplier_name,
            supplier_city,
            location_id
    ):
        supplier_id = 3
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