from flask import request
from flask_restx import Resource, abort
from src import exceptions
from src.api.resources.namespaces import NAMESPACES
from src.api.resources.users.marshallers.users_serializers import (
    user_login_serializer,
    user_roles_serializer,
    user_standard_serializer,
)
from src.api.resources.users.parsers.user_login_parser import user_login_parser
from src.api.resources.users.parsers.user_role_parser import user_role_parser
from src.api.resources.users.parsers.user_sign_up_parser import (
    user_signup_parser,
)
from src.api.resources.users.service import UserService
from src.security_utils import endpoint_allowed_roles, valid_jwt_required

user_ns = NAMESPACES["Users"]


@user_ns.route("/status")
class UserStatus(Resource):
    """User endpoint to get the status of JWT"""

    @user_ns.marshal_with(user_standard_serializer)
    @user_ns.response(200, "Success")
    @user_ns.response(400, "Bad request")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(404, "Not found")
    @user_ns.response(422, "Bad JWT signature")
    @user_ns.response(500, "Internal Server Error")
    @valid_jwt_required()
    @endpoint_allowed_roles(roles=["all"])
    def get(self):
        """check if jwt session key is still active"""
        http_response = {
            "message": "connected",
            "status": "success",
        }
        return http_response


@user_ns.route("/login")
class UserLogin(Resource):
    """Endpoint for user authentication"""

    @user_ns.marshal_with(user_login_serializer)
    @user_ns.expect(user_login_parser, validate=True)
    @user_ns.response(200, "Successfully connected")
    @user_ns.response(400, "Bad request")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(500, "Internal Server Error")
    def post(self):
        """Login user to get a valid JWT access token"""
        args = user_login_parser.parse_args(strict=True)

        try:
            user_id, jwt_token = UserService.log_in_user(args)
            http_response = {
                "status": "success",
                "message": "Successfully connected.",
                "id": user_id,
                "access_token": jwt_token,
            }
            return http_response

        except exceptions.ParameterError as e:
            user_ns.logger.warning(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(400, "Bad inputs")
        except exceptions.NotFound as e:
            user_ns.logger.warning(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(401, "Unauthorized")
        except exceptions.DBError as e:
            user_ns.logger.error(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(500, "Internal Server Error")


@user_ns.route("/signup")
class UserSignUp(Resource):
    """User endpoint to create new user"""

    @user_ns.marshal_with(user_standard_serializer)
    @user_ns.expect(user_signup_parser, validate=True)
    @user_ns.response(201, "Successfully created")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(409, "Already exists")
    @user_ns.response(500, "Internal Server Error")
    def post(self):
        """Create new user"""
        args = user_signup_parser.parse_args(strict=True)

        try:
            UserService.create_new_user(args)
            http_response = {
                "status": "success",
                "message": "Successfully created.",
            }
            return http_response, 201
        except exceptions.ParameterError as e:
            user_ns.logger.info(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(
                400,
                " name,last_name,birth_date,email, password are required !",
            )
        except exceptions.AlreadyExist as e:
            user_ns.logger.info(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(409, "Email already exists")
        except exceptions.DBError as e:
            user_ns.logger.error(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            return abort(500, "Internal Server Error")


@user_ns.route("/<int:user_id>/roles")
class UserRole(Resource):
    """User endpoint to get , add , delete user role(s)"""

    @user_ns.marshal_with(user_roles_serializer)
    @user_ns.response(200, "Success")
    @user_ns.response(500, "Internal Server Error")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(404, "Not Found")
    @user_ns.response(400, "Bad Request")
    @valid_jwt_required()
    @endpoint_allowed_roles(roles=["webshop-admin"])
    def get(self, user_id):
        """[ADMIN ONLY] List user roles"""
        try:
            user_roles = UserService().load_user_privileges(user_id)
            return user_roles
        except exceptions.NotFound as e:
            user_ns.logger.warning(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(404, "User not Found")
        except exceptions.DBError as e:
            user_ns.logger.error(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(500, "Internal server error")

    @user_ns.marshal_with(user_standard_serializer)
    @user_ns.expect(user_role_parser, validate=True)
    @user_ns.response(200, "Success")
    @user_ns.response(500, "Internal Server Error")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(404, "Not Found")
    @user_ns.response(400, "Bad Request")
    @valid_jwt_required()
    @endpoint_allowed_roles(roles=["webshop-admin"])
    def post(self, user_id):
        """[ADMIN ONLY]  Grant new roles to a user"""
        args = user_role_parser.parse_args(strict=True)
        try:
            UserService().grant_new_privileges(user_id, roles=args["roles"])
            http_resp = {
                "message": "Roles Granted Successfully",
                "status": "success",
            }
            return http_resp

        except exceptions.AlreadyExist:
            http_resp = {
                "message": "Role(s) already granted",
                "status": "No operation",
            }
            return http_resp
        except exceptions.NotFound as e:
            user_ns.logger.warning(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(404, "User or Role not found")
        except exceptions.DBError as e:
            user_ns.logger.error(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(500, "Internal server error")

    @user_ns.marshal_with(user_standard_serializer)
    @user_ns.expect(user_role_parser, validate=True)
    @user_ns.response(200, "Success")
    @user_ns.response(500, "Internal Server Error")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(404, "Not Found")
    @user_ns.response(400, "Bad Request")
    @valid_jwt_required()
    @endpoint_allowed_roles(roles=["webshop-admin"])
    def delete(self, user_id):
        """[ADMIN ONLY] Revoke one or more role(s) of a user"""
        args = user_role_parser.parse_args(strict=True)
        try:
            UserService().delete_user_privileges(user_id, roles=args["roles"])
            http_resp = {
                "message": "Roles Removed Successfully",
                "status": "success",
            }
            return http_resp
        except exceptions.NoOperation:
            http_resp = {
                "message": "Role(s) Already Not Granted",
                "status": "No operation",
            }
            return http_resp
        except exceptions.NotFound as e:
            user_ns.logger.warning(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(404, "User or role not found")
        except exceptions.ParameterError as e:
            user_ns.logger.warning(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(400, "Bad parameters")
        except exceptions.DBError as e:
            user_ns.logger.error(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(500, "Internal server error")
