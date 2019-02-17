import os

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initiliaze DB
db = SQLAlchemy(app)

# Initiliaze marshmallow
ma = Marshmallow(app)

# Product class
# TODO FIX THIS SHIZZLE
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "qty")


# Initialize schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# Create product
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get all products
@app.route("/product", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)


# Get single product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Run server
if __name__ == "__main__":
    app.run(debug=True)
