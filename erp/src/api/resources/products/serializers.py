from flask_restx import fields
from src.api.resources.namespaces import NAMESPACES

products_ns = NAMESPACES["Products"]

product_fields = {
    "id": fields.Integer(),
    "name": fields.String(),
    "quantity": fields.Integer(),
    "category": fields.String(),
    "price": fields.Float(),
}

get_serializer = products_ns.model("ProductGetSerializer", product_fields)

standard_fields = {"status": fields.String(), "message": fields.String()}

standard_serializer = products_ns.model("StandardSerializer", standard_fields)
