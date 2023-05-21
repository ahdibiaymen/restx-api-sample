from src.api.resources.customers.controller import customers_ns
from src.api.resources.products.controller import products_ns


def register_endpoints_routes(app):
    app.add_namespace(customers_ns)
    app.add_namespace(products_ns)
