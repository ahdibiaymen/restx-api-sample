from flask_restx import Resource, abort
from src import exceptions
from src.api.resources.namespaces import NAMESPACES
from src.api.resources.products.parsers import (
    filter_products,
    new_order,
    new_product,
)
from src.api.resources.products.serializers import (
    order_serializer,
    product_serializer,
    standard_serializer,
)
from src.api.resources.products.service import ProductService

products_ns = NAMESPACES["Products"]


@products_ns.route("")
class Products(Resource):
    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
    @products_ns.response(404, "Not found")
    @products_ns.response(500, "Internal server error")
    @products_ns.expect(filter_products, validate=True)
    @products_ns.marshal_with(product_serializer)
    def get(self):
        """List all products (with/without FILTERS)"""
        args = filter_products.parse_args()
        product_service = ProductService(**args)
        products = product_service.get_products()
        return products

    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
    @products_ns.response(404, "Not found")
    @products_ns.response(500, "Internal server error")
    @products_ns.expect(new_product, validate=True)
    @products_ns.marshal_with(standard_serializer)
    def post(self):
        """Create new product"""
        args = new_product.parse_args()
        product_service = ProductService()
        product = product_service.create_new_product(args)
        if product:
            http_response = {
                "status": "success",
                "message": "NEW_PRODUCT_CREATED",
            }
        else:
            http_response = {
                "status": "fail",
                "message": "FAILED_TO_CREATE_PRODUCT",
            }
        return http_response


@products_ns.route("/<int:product_id>")
class OneproductDetail(Resource):
    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
    @products_ns.response(404, "Not found")
    @products_ns.response(500, "Internal server error")
    @products_ns.marshal_with(product_serializer)
    def get(self, product_id):
        """Get one product detail"""
        product_service = ProductService()
        product = product_service.get_one_product(product_id)
        return product


@products_ns.route("/<int:product_id>/orders")
class AllproductOrders(Resource):
    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
    @products_ns.response(404, "Not found")
    @products_ns.response(500, "Internal server error")
    @products_ns.marshal_with(order_serializer)
    def get(self, product_id):
        """List all orders for a product"""
        product_service = ProductService()
        product_orders = product_service.get_product_orders(product_id)
        return product_orders

    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
    @products_ns.response(404, "Not found")
    @products_ns.response(406, "Order aborted")
    @products_ns.response(500, "Internal server error")
    @products_ns.expect(new_order, validate=True)
    @products_ns.marshal_with(standard_serializer)
    def post(self, product_id):
        """Create new order for a product"""
        args = new_order.parse_args()
        product_service = ProductService()
        try:
            product_service.create_new_order(product_id, args)
            http_response = {
                "status": "success",
                "message": "NEW_ORDER_CREATED",
            }
            return http_response
        except exceptions.NotFound as e:
            if "product_id" in e.errors.keys():
                abort(404, "Product not found")
            elif "user_id" in e.errors.keys():
                abort(404, "User not found")
        except exceptions.OrderAborted as e:
            if e.errors["reason"] == "STORAGE_LESS_THAN_QUANTITY":
                http_response = {
                    "status": "fail",
                    "message": "STORAGE_LESS_THAN_QUANTITY",
                }
                return http_response, 406


@products_ns.route("/<int:product_id>/orders/<int:order_id>")
class OneproductOrderDetail(Resource):
    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
    @products_ns.response(404, "Not found")
    @products_ns.response(500, "Internal server error")
    @products_ns.marshal_with(order_serializer)
    def get(self, product_id, order_id):
        """Get one order detail"""
        product_service = ProductService()
        try:
            order = product_service.get_one_order(product_id, order_id)
            return order
        except exceptions.NotFound:
            abort(404, "Order not found")
