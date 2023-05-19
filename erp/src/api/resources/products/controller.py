from flask_restx import Resource
from src.api.resources.namespaces import NAMESPACES
from src.api.resources.products.parsers import filter_products, new_product
from src.api.resources.products.serializers import (
    get_serializer,
    standard_serializer,
)
from src.api.resources.products.service import ProductService

products_ns = NAMESPACES["Products"]


@products_ns.route("")
class Products(Resource):
    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
    @products_ns.response(500, "Internal server error")
    @products_ns.expect(filter_products, validate=True)
    @products_ns.marshal_with(get_serializer)
    def get(self):
        """List all products (with/without FILTERS)"""
        args = filter_products.parse_args()
        product_service = ProductService(**args)
        products = product_service.get_products()
        return products

    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
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
    @products_ns.response(500, "Internal server error")
    @products_ns.marshal_with(get_serializer)
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
    @products_ns.response(500, "Internal server error")
    def get(self):
        """List all orders for a product"""
        pass

    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
    @products_ns.response(500, "Internal server error")
    def post(self):
        """Create new order for a product"""
        pass


@products_ns.route("/<int:product_id>/orders/<int:order_id>")
class OneproductOrderDetail(Resource):
    @products_ns.response(200, "Success")
    @products_ns.response(400, "Bad request")
    @products_ns.response(401, "Unauthorized")
    @products_ns.response(500, "Internal server error")
    def get(self):
        """Get one order detail"""
        pass
