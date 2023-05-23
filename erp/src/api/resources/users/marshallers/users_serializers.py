from flask_restx import fields
from src.api.resources.namespaces import NAMESPACES

user_ns = NAMESPACES["Users"]

user_standard_serializer = user_ns.model(
    "UserStandard",
    {
        "message": fields.String(),
        "status": fields.String(),
    },
)

user_roles_serializer = user_ns.model(
    "UserRoles",
    {
        "user_id": fields.String(),
        "user_roles": fields.List(fields.String),
    },
)

user_login_serializer = user_ns.model(
    "UserLogin",
    {
        "message": fields.String(),
        "status": fields.String(),
        "id": fields.String(),
        "access_token": fields.String(),
    },
)

user_apikey_serializer = user_ns.model(
    "UserApikey",
    {
        "api_key": fields.String(),
    },
)
