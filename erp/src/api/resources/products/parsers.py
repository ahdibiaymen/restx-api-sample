from flask_restx import reqparse

filter_products = reqparse.RequestParser()
filter_products.add_argument(
    "name",
    type=str,
    location="args",
    required=False,
    nullable=True,
)
filter_products.add_argument(
    "category",
    type=str,
    location="args",
    required=False,
    nullable=True,
)

new_product = reqparse.RequestParser()
new_product.add_argument(
    "name",
    type=str,
    location="json",
    required=True,
    nullable=False,
)
new_product.add_argument(
    "quantity",
    type=int,
    location="json",
    required=True,
    nullable=False,
)
new_product.add_argument(
    "category",
    type=str,
    location="json",
    required=True,
    nullable=False,
)
new_product.add_argument(
    "price",
    type=int,
    location="json",
    required=True,
    nullable=False,
)
