from flask_restx import Resource

from ..namespaces import NAMESPACES

customers_ns = NAMESPACES["Customers"]


@customers_ns.route("")
class Customers(Resource):
    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(500, "Internal server error")
    def get(self):
        """List all customers"""
        pass

    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(500, "Internal server error")
    def post(self):
        """Create new customer"""
        pass


@customers_ns.route("/<int:customer_id>")
class OneCustomerDetail(Resource):
    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(500, "Internal server error")
    def get(self):
        """Get one customer detail"""
        pass


@customers_ns.route("/<int:customer_id>/orders")
class AllCustomerOrders(Resource):
    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(500, "Internal server error")
    def get(self):
        """List all orders for a customer"""
        pass

    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(500, "Internal server error")
    def post(self):
        """Create new order for a customer"""
        pass


@customers_ns.route("/<int:customer_id>/orders/<int:order_id>")
class OneCustomerOrderDetail(Resource):
    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(500, "Internal server error")
    def get(self):
        """Get one order detail"""
        pass


@customers_ns.route("/<int:customer_id>/orders/<int:order_id>/products")
class OneCustomerOrderProductDetail(Resource):
    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(500, "Internal server error")
    def get(self):
        """List all products for an order"""
        pass

    @customers_ns.response(200, "Success")
    @customers_ns.response(400, "Bad request")
    @customers_ns.response(401, "Unauthorized")
    @customers_ns.response(500, "Internal server error")
    def post(self):
        """Add a product for an order"""
        pass
