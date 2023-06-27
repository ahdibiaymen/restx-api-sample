from flask_restx import inputs, reqparse

user_signup_parser = reqparse.RequestParser()
user_signup_parser.add_argument(
    "name",
    type=str,
    location="json",
    required=True,
    trim=True,
)
user_signup_parser.add_argument(
    "last_name",
    type=str,
    location="json",
    required=True,
    trim=True,
)
user_signup_parser.add_argument(
    "email",
    type=str,
    location="json",
    required=True,
    nullable=False,
    trim=True,
)
user_signup_parser.add_argument(
    "password",
    type=str,
    location="json",
    required=True,
    nullable=False,
    trim=True,
)
user_signup_parser.add_argument(
    "birth_date", type=inputs.date_from_iso8601, location="json", required=True
)
