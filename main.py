from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from api.handlers.product_handler import ProductHandler
from api.handlers.customer_handler import CustomerHandler
from api.handlers.user_handler import UserHandler
from api.handlers.request_handler import RequestHandler

app = Flask(__name__)
CORS(app)


@app.route("/")
def greet():
    return "Disaster Storage Database"


### USERS ###


@app.route("/disasterStorage/users", methods=["GET"])
def get_all_users():
    if request.method == "GET":
        return UserHandler().get_all_users()
    return


@app.route("/disasterStorage/users/<int:user_id>", methods=["GET", "PUT"])
def get_user_by_id(user_id):
    if request.method == "GET":
        return UserHandler().get_user_by_id(user_id)

    elif request.method == "PUT":
        return

    else:
        return


### CUSTOMERS ###


@app.route("/disasterStorage/users/customers", methods=["GET", "POST"])
def get_all_customers():
    return


@app.route("/disasterStorage/users/<int:customer_id>", methods=["GET", "PUT", "DELETE"])
def get_customer_by_id(customer_id):
    return


### SUPPLIERS ###


@app.route("/disasterStorage/users/suppliers")
def get_all_suppliers():
    return


@app.route("/disasterStorage/users/<int:supplier_id>")
def get_supplier_by_id(supplier_id):
    return

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


### REQUESTS ###

@app.route("/disasterStorage/requests", methods=["GET", "POST"])
def get_all_requests():
    if request.method == "GET":
        if not request.args:
            return RequestHandler().get_all_requests()

        return RequestHandler().search_requests(request.args)

    if request.method == "POST":
        return RequestHandler().insert_request(request.json);


@app.route("/disasterStorage/requests/<int:request_id>", methods=["GET", "PUT", "DELETE"])
def get_request_by_id(request_id):
    if request.method == "GET":
        return RequestHandler().get_request_by_id(request_id)

    if request.method == "PUT":
        return RequestHandler().update_request(request_id, request.json)

    if request.method == "DELETE":
        return RequestHandler().delete_request(request_id)

@app.route("/disasterStorage/requests/products/<int:product_id>")
def get_requests_by_product_id(product_id):
    if request.method == "GET":
        return RequestHandler().get_requests_by_product_id(product_id)

@app.route("/disasterStorage/requests/customers/<int:customer_id>")
def get_requests_by_customer_id(customer_id):
    if request.method == "GET":
        return RequestHandler().get_requests_by_customer_id(customer_id)


if __name__ == "__main__":
    app.run()
