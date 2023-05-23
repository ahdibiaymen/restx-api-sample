from flask_restx import reqparse

filter_customers = reqparse.RequestParser()
filter_customers.add_argument(
    "name_filter",
    type=str,
    location="args",
    required=False,
    nullable=True,
)
filter_customers.add_argument(
    "last_name_filter",
    type=str,
    location="args",
    required=False,
    nullable=True,
)
filter_customers.add_argument(
    "email_filter",
    type=str,
    location="args",
    required=False,
    nullable=True,
)
