from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from api.handlers.product_handler import ProductHandler
from api.handlers.admin_handler import AdminHandler
from api.handlers.customer_handler import CustomerHandler
from api.handlers.supplier_handler import SupplierHandler
from api.handlers.user_handler import UserHandler
from api.handlers.request_handler import RequestHandler
from api.handlers.reservation_handler import ReservationHandler
from api.handlers.order_handler import OrderHandler

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

    elif request.method == "POST":
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


@app.route("/disasterStorage/users/admin/<int:admin_id>", methods=["GET", "PUT", "DELETE"])
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

    elif request.method == "POST":
        return CustomerHandler().insert_customer(request.json)


@app.route(
    "/disasterStorage/users/customers/<int:customer_id>",
    methods=["GET", "PUT", "DELETE"],
)
def get_customer_by_id(customer_id):
    if request.method == "GET":
        return CustomerHandler().get_customer_by_id(customer_id)

    elif request.method == "PUT":
        return CustomerHandler().update_customer(customer_id, request.json)

    else:
        return CustomerHandler().delete_customer(customer_id)

@app.route(
    "/disasterStorage/users/customers/<int:customer_id>/location", methods=["GET"],
)
def get_customer_location_by_id(customer_id):
    return CustomerHandler().get_customer_location_by_id(customer_id)

@app.route(
    "/disasterStorage/users/customers/<int:customer_id>/creditCards", methods=["GET"],
)
def get_customer_ccard_by_id(customer_id):
    return CustomerHandler().get_customer_ccard_by_id(customer_id)

@app.route( "/disasterStorage/users/customers/<int:customer_id>/products/ordered", methods=["GET"],)
def get_product_ordered_by_customer(customer_id):
    return CustomerHandler().get_product_ordered_by_customer(customer_id)

@app.route( "/disasterStorage/users/customers/<int:customer_id>/products/reserved", methods=["GET"],)
def get_product_reserved_by_customer(customer_id):
    return CustomerHandler().get_product_reserved_by_customer(customer_id)

@app.route( "/disasterStorage/users/customers/<int:customer_id>/products/requested", methods=["GET"],)
def get_product_requested_by_customer(customer_id):
    return CustomerHandler().get_product_requested_by_customer(customer_id)

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


@app.route(
    "/disasterStorage/users/suppliers/<int:supplier_id>",
    methods=["GET", "PUT", "DELETE"],
)
def get_supplier_by_id(supplier_id):
    if request.method == "GET":
        return SupplierHandler().get_supplier_by_id(supplier_id)

    elif request.method == "PUT":
        return SupplierHandler().update_supplier(supplier_id, request.json)

    else:
        return SupplierHandler().delete_supplier(supplier_id)

@app.route(
    "/disasterStorage/users/supplier/<int:supplier_id>/products", methods=["GET"],
)
def get_product_by_supplier_id(supplier_id):
    return SupplierHandler().get_products_by_supplier_id(supplier_id)

@app.route(
    "/disasterStorage/users/supplier/<int:supplier_id>/location", methods=["GET"],
)
def get_supplier_location_by_id(supplier_id):
    return SupplierHandler().get_supplier_location(supplier_id)

### PRODUCT ###

@app.route("/disasterStorage/products", methods=["GET", "POST"])
def get_all_products():
    if request.method == "GET":
        if not request.args:
            return ProductHandler().get_all_products()

        else:
            return ProductHandler().search_products(request.args)

    elif request.method == "POST":
        return ProductHandler().insert_product(request.json)


@app.route("/disasterStorage/products/<string:category>")
def get_all_products_by_category(category):
    return ProductHandler().get_all_products_by_category(category)


@app.route(
    "/disasterStorage/products/<int:product_id>", methods=["GET", "PUT", "DELETE"]
)
def get_product_by_id(product_id):
    if request.method == "GET":
        return ProductHandler().get_product_by_id(product_id)

    elif request.method == "PUT":
        return ProductHandler().update_product(product_id, request.json)

    else:
        return ProductHandler().delete_product(product_id)


@app.route("/disasterStorage/products/<int:product_id>/details", methods=["GET", "PUT"])
def get_product_details(product_id):
    if request.method == "GET":
        return ProductHandler().get_detailed_product_by_id(product_id)
    else:
        return ProductHandler().update_product_category_info(product_id, request.json)


@app.route(
    "/disasterStorage/products/<int:product_id>/location", methods=["GET", "PUT"]
)
def get_product_location(product_id):
    if request.method == "GET":
        return ProductHandler().get_product_location(product_id)
    else:
        return ProductHandler().update_product_location(product_id, request.json)


### ORDERS ###


@app.route("/disasterStorage/orders", methods=["GET", "POST"])
def get_all_orders():
    if request.method == "GET":
        return OrderHandler().get_all_orders()
    if request.method == "POST":
        return OrderHandler().insert_order(request.json)

@app.route("/disasterStorage/orders/<int:order_id>", methods=["GET", "PUT", "DELETE"])
def get_order_by_id(order_id):
    if request.method == "GET":
        return OrderHandler().get_order_by_id(order_id)
    if request.method == "PUT":
        return OrderHandler().update_order(order_id, request.json)
    if request.method == "DELETE":
        return OrderHandler().delete_order(order_id)

@app.route("/disasterStorage/orders/<int:order_id>/add", methods=["POST"])
def insert_product_to_order(order_id):
    return OrderHandler().add_product(order_id, request.json)

@app.route("/disasterStorage/orders/products/<int:product_id>")
def get_orders_by_product(product_id):
    if request.method == "GET":
        return OrderHandler().get_orders_by_product_id(product_id)


@app.route("/disasterStorage/orders/customers/<int:customer_id>", methods=["GET", "DELETE"])
def get_orders_by_customer(customer_id):
    if request.method == "GET":
        return OrderHandler().get_orders_by_customer_id(customer_id)
    if request.method == "DELETE":
        return OrderHandler().delete_order_by_customer_id(customer_id)

### RESERVATIONS ###


@app.route("/disasterStorage/reservations", methods=["GET", "POST"])
def get_all_reservations():
    if request.method == "GET":
        return ReservationHandler().get_all_reservations()

    if request.method == "POST":
        return ReservationHandler().insert_reservation(request.json)


@app.route(
    "/disasterStorage/reservations/<int:reservation_id>",
    methods=["GET", "PUT", "DELETE"],
)
def get_reservation_by_id(reservation_id):
    if request.method == "GET":
        return ReservationHandler().get_reservation_by_id(reservation_id)

    if request.method == "PUT":
        return ReservationHandler().update_reservation(reservation_id, request.json)

    if request.method == "DELETE":
        return ReservationHandler().delete_reservation(reservation_id)


@app.route("/disasterStorage/reservations/<int:reservation_id>/add", methods=["POST"])
def insert_product_to_reservation(reservation_id):
    return ReservationHandler().add_product(reservation_id, request.json)


@app.route("/disasterStorage/reservations/products/<int:product_id>")
def get_reservations_by_product(product_id):
    if request.method == "GET":
        return ReservationHandler().get_reservations_by_product_id(product_id)


@app.route("/disasterStorage/reservations/customers/<int:customer_id>", methods=["GET", "DELETE"])
def get_reservations_by_customer(customer_id):
    if request.method == "GET":
        return ReservationHandler().get_reservations_by_customer_id(customer_id)
    if request.method == "DELETE":
        return ReservationHandler().delete_reservations_by_customer_id(customer_id)


### REQUESTS ###


@app.route("/disasterStorage/requests", methods=["GET", "POST"])
def get_all_requests():
    if request.method == "GET":
        if not request.args:
            return RequestHandler().get_all_requests()

        return RequestHandler().search_requests(request.args)

    if request.method == "POST":
        return RequestHandler().insert_request(request.json)


@app.route(
    "/disasterStorage/requests/<int:request_id>", methods=["GET", "PUT", "DELETE"]
)
def get_request_by_id(request_id):
    if request.method == "GET":
        return RequestHandler().get_request_by_id(request_id)

    if request.method == "PUT":
        return RequestHandler().update_request(request_id, request.json)

    if request.method == "DELETE":
        return RequestHandler().delete_request(request_id)


@app.route(
    "/disasterStorage/requests/<int:request_id>/add", methods=["POST"]
)
def add_product_to_request(request_id):
    return RequestHandler().add_product(request_id, request.json)


@app.route("/disasterStorage/requests/products/<int:product_id>")
def get_requests_by_product_id(product_id):
    if request.method == "GET":
        return RequestHandler().get_requests_by_product_id(product_id)


@app.route("/disasterStorage/requests/customers/<int:customer_id>", methods=["GET", "DELETE"])
def get_requests_by_customer_id(customer_id):
    if request.method == "GET":
        return RequestHandler().get_requests_by_customer_id(customer_id)
    if request.method == "DELETE":
        return RequestHandler().delete_requests_by_customer_id(customer_id)
