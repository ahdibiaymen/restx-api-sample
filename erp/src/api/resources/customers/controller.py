from flask_restx import Resource, abort
from src import exceptions
from src.api.resources.customers.parsers import filter_customers
from src.api.resources.customers.serializers import (
    customer_serializer,
    order_serializer,
    product_serializer,
)
from src.api.resources.customers.service import CustomersService
from src.api.resources.namespaces import NAMESPACES
from src.security_utils import endpoint_allowed_roles, valid_jwt_required

customers_ns = NAMESPACES["Customers"]


@customers_ns.route("")
class Customers(Resource):
    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(500, "Internal server error")
    @customers_ns.expect(filter_customers, validate=True)
    @customers_ns.marshal_with(customer_serializer)
    @valid_jwt_required()
    @endpoint_allowed_roles(roles=["webshop-admin"])
    def get(self):
        """List all customers"""
        args = filter_customers.parse_args()
        customerservice = CustomersService(**args)
        customers = customerservice.get_customers()
        return customers


@customers_ns.route("/<int:customer_id>")
class OneCustomerDetail(Resource):
    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(404, "Not Found")
    @customers_ns.response(500, "Internal server error")
    @customers_ns.marshal_with(customer_serializer)
    @valid_jwt_required()
    @endpoint_allowed_roles(roles=["webshop-admin"])
    def get(self, customer_id):
        """Get one customer detail"""
        customerservice = CustomersService()
        try:
            customer = customerservice.get_one_customer(customer_id)
        except exceptions.NotFound:
            abort(404, "Not Found")
        else:
            return customer


@customers_ns.route("/<int:customer_id>/orders")
class AllCustomerOrders(Resource):
    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(404, "Not Found")
    @customers_ns.response(500, "Internal server error")
    @customers_ns.marshal_with(order_serializer)
    @valid_jwt_required()
    @endpoint_allowed_roles(roles=["webshop-admin"])
    def get(self, customer_id):
        """List all orders for a customer"""
        customerservice = CustomersService()
        try:
            orders = customerservice.get_customer_orders(customer_id)
        except exceptions.NotFound:
            abort(404, "Not Found")
        else:
            return orders


@customers_ns.route("/<int:customer_id>/orders/<int:order_id>/product")
class OneCustomerOrderProductDetail(Resource):
    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(404, "Not Found")
    @customers_ns.response(500, "Internal server error")
    @customers_ns.marshal_with(product_serializer)
    @valid_jwt_required()
    @endpoint_allowed_roles(roles=["webshop-admin"])
    def get(self, customer_id, order_id):
        """get order product detail"""
        customerservice = CustomersService()
        try:
            order_detail = customerservice.get_customer_order_detail(
                customer_id, order_id
            )
        except exceptions.NotFound:
            abort(404, "Not Found")
        else:
            return order_detail
