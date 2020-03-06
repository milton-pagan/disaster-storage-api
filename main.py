from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	return "Hello, world!"



if __name__ == "__main__":
	app.run()
