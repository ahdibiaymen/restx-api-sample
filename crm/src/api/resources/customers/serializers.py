from flask_restx import fields
from src.api.resources.namespaces import NAMESPACES

customers_ns = NAMESPACES["Customers"]

customer_fields = {
    "id": fields.Integer(),
    "birthdate": fields.DateTime(),
    "name": fields.String(),
    "last_name": fields.String(),
    "email": fields.String(),
}

customer_serializer = customers_ns.model(
    "CustomerGetSerializer", customer_fields
)

order_fields = {
    "user": fields.String(),
    "product": fields.String(),
    "order_id": fields.Integer(),
    "order_date": fields.DateTime(),
    "order_quantity": fields.Integer(),
    "order_price": fields.Float(),
}

order_serializer = customers_ns.model("OrderSerializer", order_fields)


product_fields = {
    "id": fields.Integer(),
    "name": fields.String(),
    "quantity": fields.Integer(),
    "category": fields.String(),
    "price": fields.Float(),
}

product_serializer = customers_ns.model("ProductGetSerializer", product_fields)
