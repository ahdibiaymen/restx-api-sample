from flask_restx import Namespace

NAMESPACES = {
    "Customers": Namespace(
        "customers", description="endpoint for operations related to customers"
    ),
}
