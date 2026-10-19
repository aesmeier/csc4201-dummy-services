import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from logging_helper import log_event
import os

app = Flask(__name__)
CORS(app, origins=[
    os.environ.get('CORS_LOCALHOST', 'http://localhost:5173'),
    os.environ.get('CORS_URL', 'https://frontend-service-887823769496.us-central1.run.app')
])
logging.basicConfig(level=logging.INFO)

PRODUCTS = [
    {"product_id": "1", "name": "Wireless Mouse", "description": "A smooth wireless mouse", "price": 19.99, "categories": ["electronics", "accessories"]},
    {"product_id": "2", "name": "Mechanical Keyboard", "description": "RGB mechanical keyboard", "price": 59.99, "categories": ["electronics", "accessories"]},
    {"product_id": "3", "name": "Coffee Mug", "description": "Ceramic mug for coffee lovers", "price": 9.99, "categories": ["kitchen"]},
    {"product_id": "4", "name": "Desk Lamp", "description": "LED desk lamp", "price": 24.99, "categories": ["home", "electronics"]},
    {"product_id": "5", "name": "Notebook", "description": "Ruled paper notebook", "price": 4.99, "categories": ["office"]},
    {"product_id": "6", "name": "Backpack", "description": "Laptop backpack", "price": 39.99, "categories": ["accessories", "travel"]},
    {"product_id": "7", "name": "Water Bottle", "description": "Insulated steel bottle", "price": 14.99, "categories": ["kitchen", "travel"]},
    {"product_id": "8", "name": "Headphones", "description": "Noise-cancelling headphones", "price": 89.99, "categories": ["electronics"]},
]


@app.route("/products")
def list_products():
    search = request.args.get("search", "")
    log_event(app.logger, f"GET /products search={search!r}")
    if not search:
        return jsonify(PRODUCTS)
    needle = search.lower()
    results = [
        p for p in PRODUCTS
        if needle in p["name"].lower() or needle in p["description"].lower()
    ]
    return jsonify(results)


@app.route("/products/<product_id>")
def get_product(product_id):
    log_event(app.logger, f"GET /products/{product_id}")
    for p in PRODUCTS:
        if p["product_id"] == product_id:
            return jsonify(p)
    log_event(app.logger, f"product {product_id} not found")
    return jsonify({"error": "not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))