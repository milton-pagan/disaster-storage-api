from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

@app.route('/')
def greet():
	return "Disaster Storages Database"

### USERS ###

@app.route('/disasterStorage/users', methods=['POST'])
def get_all_users():
	return "Dummy return"

@app.route('/disasterStorage/users/<int:user_id>')
def get_user_by_id(user_id):
	return

### CUSTOMERS ###

@app.route('/disasterStorage/users/customers')
def get_all_customers():
	return

@app.route('/disasterStorage/users/<int:customer_id>')
def get_customer_by_id(customer_id):
	return

### SUPPLIERS ###

@app.route('/disasterStorage/users/suppliers')
def get_all_suppliers():
	return

@app.route('/disasterStorage/users/<int:supplier_id>')
def get_supplier_by_id(supplier_id):
	return

### REQUESTS ###

@app.route('/disasterStorage/requests', methods=['GET', 'POST'])
def get_all_requests():
	return

@app.route('/disasterStorage/requests/products')
def get_all_requested_products():
	if not request.args:
		return 'Req Prods'

	else:
		return 'Keyword search'

### PRODUCTS ###

@app.route('/disasterStorage/products', methods=['GET', 'POST', 'PUT'])
def get_all_products():
	if not request.args:
		return "Undetailed"

	elif request.method  == 'GET' and 'd' in request.args:
		return "detailed product"

	
	return

@app.route('/disasterStorage/products/<int:product_id>')
def get_product_by_id(product_id):
	return

@app.route('/disasterStorage/products/available')
def get_available_products():
	if not request.args:
		return 'Avail Prods'

	else:
		return 'Keyword search avail'



if __name__ == "__main__":
	app.run()
