from src.api.resources.customers.controller import customers_ns
from src.api.resources.prospects.controller import prospects_ns
from src.api.resources.users.controller import user_ns


def register_endpoints_routes(app):
    app.add_namespace(customers_ns)
    app.add_namespace(prospects_ns)
    app.add_namespace(user_ns)
