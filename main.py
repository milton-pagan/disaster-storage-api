from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from ds_app.handlers.product_handler import ProductHandler
from ds_app.handlers.customer_handler import CustomerHandler

app = Flask(__name__)
CORS(app)


@app.route("/")
def greet():
    return "Disaster Storage Database"


### USERS ###


@app.route("/disasterStorage/users", methods=["GET"])
def get_all_users():
    return "Dummy return"


@app.route("/disasterStorage/users/<int:user_id>")
def get_user_by_id(user_id):
    return


### CUSTOMERS ###


@app.route("/disasterStorage/users/customers", methods=["GET", "POST"])
def get_all_customers():
    if request.method == "GET":
        return "all customers"

    else:
        print("PAYLOAD:", request.json)
        return CustomerHandler().add_customer(request.json)
    return


@app.route("/disasterStorage/users/<int:customer_id>")
def get_customer_by_id(customer_id):
    return


### SUPPLIERS ###


@app.route("/disasterStorage/users/suppliers")
def get_all_suppliers():
    return


@app.route("/disasterStorage/users/<int:supplier_id>")
def get_supplier_by_id(supplier_id):
    return


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
        else:
            return ProductHandler().search_product(request.args)

    elif request.method == "POST":
        pass


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
        return

    else:
        return


# DEPRECATED
@app.route("/disasterStorage/products/available")
def get_available_products():
    if not request.args:
        return ProductHandler().get_available_products()

    else:
        return "Keyword search avail"


if __name__ == "__main__":
    app.run()
