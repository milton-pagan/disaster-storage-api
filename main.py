from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from api.handlers.product_handler import ProductHandler
from api.handlers.admin_handler import AdminHandler
from api.handlers.customer_handler import CustomerHandler
from api.handlers.supplier_handler import SupplierHandler
from api.handlers.user_handler import UserHandler

app = Flask(__name__)
CORS(app)


@app.route("/")
def greet():
    return "Disaster Storage Database"


### USERS ###


@app.route("/disasterStorage/users", methods=["GET", "POST"])
def get_all_users():
    if request.method == "GET":
        return UserHandler().get_all_users()

    elif request == "POST":
        return UserHandler().insert_user(request.json)


@app.route("/disasterStorage/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def get_user_by_id(user_id):
    if request.method == "GET":
        return UserHandler().get_user_by_id(user_id)

    elif request.method == "PUT":
        return UserHandler().updated_user(user_id, request.json)

    else:
        return UserHandler().delete_user(user_id)


### ADMIN ###


@app.route("/disasterStorage/users/admin", methods=["GET", "POST"])
def get_all_admins():
    if request.method == "GET":
        return AdminHandler().get_all_admins()
    elif request.method == "POST":
        return AdminHandler().insert_admin(request.json)


@app.route("/disasterStorage/users/admin", methods=["GET", "PUT", "DELETE"])
def get_admin_by_id(admin_id):
    if request.method == "GET":
        return AdminHandler().get_admin_by_id(admin_id)

    elif request.method == "PUT":
        return AdminHandler().update_admin(admin_id, request.json)

    else:
        return AdminHandler().delete_admin(admin_id)


### CUSTOMERS ###


@app.route("/disasterStorage/users/customers", methods=["GET", "POST"])
def get_all_customers():
    if request.method == "GET":
        if not request.args:
            return CustomerHandler().get_all_customers()
        else:
            return CustomerHandler().search_customer(request.args)

    elif request == "POST":
        return CustomerHandler().insert_customer(request.json)


@app.route("/disasterStorage/users/customers/<int:customer_id>", methods=["GET", "PUT", "DELETE"])
def get_customer_by_id(customer_id):
    if request.method == "GET":
        return CustomerHandler().get_customer_by_id(customer_id)

    elif request.method == "PUT":
        return CustomerHandler().update_customer(customer_id, request.json)

    else:
        return CustomerHandler().delete_customer(customer_id)


### SUPPLIERS ###


@app.route("/disasterStorage/users/suppliers", methods=["GET", "POST"])
def get_all_suppliers():
    if request.method == "GET":
        if not request.args:
            return SupplierHandler().get_all_suppliers()
        else:
            return SupplierHandler().search_suppliers(request.args)

    elif request == "POST":
        return SupplierHandler().insert_supplier(request.json)


@app.route("/disasterStorage/users/suppliers/<int:supplier_id>", methods=["GET", "PUT", "DELETE"])
def get_supplier_by_id(supplier_id):
    if request.method == "GET":
        return SupplierHandler().get_supplier_by_id(supplier_id)

    elif request.method == "PUT":
        return SupplierHandler().update_supplier(supplier_id, request.json)

    else:
        return SupplierHandler().delete_supplier(supplier_id)


### REQUESTS ###


@app.route("/disasterStorage/requests", methods=["GET", "POST"])
def get_all_requests():
    return


@app.route("/disasterStorage/requests/products")
def get_all_requested_products():
    if not request.args:
        return "Req Prods"

    else:
        return "Keyword search"


### PRODUCTS ###


@app.route("/disasterStorage/products", methods=["GET", "POST"])
def get_all_products():
    if request.method == "GET":
        if not request.args:
            return ProductHandler().get_all_products()
        elif "d" in request.args:
            return ProductHandler().get_all_detailed_products()

    elif request.method == "POST":
        return ProductHandler().insert_product(request.json)


@app.route(
    "/disasterStorage/products/<int:product_id>", methods=["GET", "PUT", "DELETE"]
)
def get_product_by_id(product_id):
    if request.method == "GET":
        if "d" in request.args:
            return ProductHandler().get_detailed_product_by_id(product_id)
        else:
            return ProductHandler().get_product_by_id(product_id)

    elif request.method == "PUT":
        return ProductHandler().update_product(product_id, request.json)

    else:
        return ProductHandler().delete_product(product_id)


@app.route("/disasterStorage/products/available")
def get_available_products():
    if not request.args:
        return ProductHandler().get_available_products()

    else:
        if 'd' in request.args:
            return ProductHandler().get_detailed_available_products()
        else:
            return ProductHandler().search_available_product(request.args)


if __name__ == "__main__":
    app.run()
