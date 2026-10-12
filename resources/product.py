import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from db import products, stores
from schemas import ProductSchema, ProductUpdateSchema

blp = Blueprint("products", __name__, description="Operations on products")

@blp.route("/product/<string:product_id>")
class Product(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        try:
            return products[product_id]
        except KeyError:
            abort(404, message="Product not found.")

    @jwt_required()
    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductSchema)
    def put(self, product_data, product_id):
        try:
            product = products[product_id]
            product.update(product_data)
            return product
        except KeyError:
            abort(404, message="Product not found.")

    @jwt_required()
    def delete(self, product_id):
        try:
            del products[product_id]
            return {"message": "Product deleted."}
        except KeyError:
            abort(404, message="Product not found.")

@blp.route("/product")
class ProductList(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        return list(products.values())

    @jwt_required()
    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        if product_data["store_id"] not in stores:
            abort(404, message="Store not found.")
        product_id = uuid.uuid4().hex
        product = {**product_data, "id": product_id}
        products[product_id] = product
        return product
