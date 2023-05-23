from flask_restx import Namespace

NAMESPACES = {
    "Customers": Namespace(
        "customers", description="endpoint for operations related to customers"
    ),
    "Products": Namespace(
        "products", description="endpoint for operations related to products"
    ),
    "Users": Namespace(
        "users", description="endpoint for operations related to users"
    ),
}
