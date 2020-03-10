from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

@app.route('/')
def greet():
	return "Disaster Storages Database"

### USERS ###

@app.route('/disaster_app/user', methods=['POST'])
def get_all_users():
	return "Dummy return"

@app.route('/disaster_app/user/<int:user_id>')
def get_user_by_id(user_id):
	return

### CUSTOMERS ###

@app.route('/disaster_app/user/customer')
def get_all_customers():
	return

@app.route('/disaster_app/user/<int:customer_id>')
def get_customer_by_id(customer_id):
	return

### SUPPLIERS ###

@app.route('/disaster_app/user/supplier')
def get_all_suppliers():
	return

@app.route('/disaster_app/user/<int:supplier_id>')
def get_supplier_by_id(supplier_id):
	return

### REQUESTS ###

@app.route('/disaster_app/request', methods=['GET', 'POST'])
def get_all_requests():
	return

@app.route('/disaster_app/request/product')
def get_all_requested_products():
	if not request.args:
		return 'Req Prods'

	else:
		return 'Keyword search'

### PRODUCTS ###

@app.route('/disaster_app/product', methods=['GET', 'POST', 'PUT'])
def get_all_products():
	if not request.args:
		return "Undetailed"

	elif request.method  == 'GET' and 'd' in request.args:
		return "detailed product"

	
	return

@app.route('/disaster_app/product/<int:product_id>')
def get_product_by_id(product_id):
	return

@app.route('/disaster_app/product/available')
def get_available_products():
	if not request.args:
		return 'Avail Prods'

	else:
		return 'Keyword search avail'



if __name__ == "__main__":
	app.run()
