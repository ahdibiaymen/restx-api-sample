from flask_restx import reqparse

user_role_parser = reqparse.RequestParser()

user_role_parser.add_argument(
    "roles",
    type=list,
    help="users role(s) to be Granted/Revoked",
    location="json",
    required=True,
    nullable=False,
)
