import hashlib
from functools import wraps
from logging import getLogger

from flask import current_app
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restx import abort
from src import exceptions, models
from src.default_config import DefaultConfig

logger = getLogger("CRM_api")


def hash_and_salt_password(string):
    if not string:
        raise ValueError("Password required")
    # salting
    string += DefaultConfig.ERP_PASSWORD_SALT
    return hashlib.sha512(string.encode()).hexdigest()


def verify_password(password, db_hash):
    if not db_hash or not password:
        raise ValueError("Password & db_hash is required")
    # checking
    password_hash = hash_and_salt_password(password)
    return password_hash == db_hash


def load_user_from_request():
    """load user object from JWT key"""
    with current_app.app_context():
        try:
            verify_jwt_in_request()
        except NoAuthorizationError:
            abort(401, "Missing Authorization Header")
        jwt_identity = get_jwt_identity()
        if not jwt_identity.get("user_id", False):
            raise exceptions.BadJWTSignature(
                action="LOAD_USER_FROM_REQUEST",
                jwt_identity=jwt_identity,
                reason="BAD_PAYLOAD",
            )

        user_id = jwt_identity["user_id"]

        try:
            user = models.User.get_user_by_id(user_id)
            if user:
                return user
            else:
                return None
        except exceptions.DBError as e:
            logger.error(
                "Load_user_from_request caused the following exception "
                f" exception: {e}"
            )
            abort(500, "Internal Server Error")


def endpoint_allowed_roles(roles):
    """check if a user have the rights to access
    an endpoint according to 'roles' parameter
    """

    def main_decorator(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            ALL_ROLES = ["webshop-admin", "webshop-client", "reseller"]
            user = None
            try:
                user = load_user_from_request()
            except exceptions.BadJWTSignature as e:
                logger.warning(
                    "Unauthorized access by unknown user caused the following"
                    f" exception  exception: {e}"
                )
                abort(422, "Bad JWT signature")
            if not user:
                abort(401, "Unable to identify user")

            try:
                user_roles = user.get_user_roles()
                if "all" in roles:
                    authorized_roles = ALL_ROLES
                else:
                    authorized_roles = roles
                for allowed_role in authorized_roles:
                    if allowed_role in user_roles:
                        return f(*args, **kwargs)

                abort(401, "Insufficient rights to access this endpoint")
            except exceptions.DBError as e:
                logger.error(
                    "endpoint_allowed_roles caused the following exception "
                    f" exception: {e}"
                )
                abort(500, "Internal server error")

        return decorator

    return main_decorator


def valid_jwt_required():
    """check JWT validity and signature"""

    def main_decorator(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except NoAuthorizationError:
                abort(401, "Missing Authorization Header")

            identity = get_jwt_identity()
            if not isinstance(identity, dict):
                abort(422, "Invalid JWT token")
            if not identity.get("user_id", False):
                abort(401, "Invalid JWT token, please re-authenticate")

            user_id = identity["user_id"]
            try:
                user = models.User.get_user_by_id(user_id)
                if not user:
                    abort(401, "Invalid JWT token, please re-authenticate")
                return f(*args, **kwargs)
            except exceptions.NotFound as e:
                logger.warning(
                    "Unauthorized access by unknown user caused the following"
                    f" exception  exception: {e}"
                )
                abort(401, "Unauthorized")
            except exceptions.DBError as e:
                logger.error(
                    "valid_jwt_required caused the following exception "
                    f" exception: {e}"
                )
                abort(500, "Internal server error")

        return decorator

    return main_decorator


def idor_protection(requested_id_object):
    """access control protection against
    'Insecure direct object references (IDOR)' vulnerability
    Authenticated user has access to only his resources, ADMIN has full access
    """
    request_user = load_user_from_request()
    if not request_user:
        raise exceptions.UnauthorizedAccess(
            action="IDOR_PROTECTION",
            object_id=requested_id_object,
            reason="CANNOT_LOAD_USER",
        )

    # ADMIN can request everything
    if not request_user.is_admin():
        if not requested_id_object == request_user.id:
            raise exceptions.UnauthorizedAccess(
                action="IDOR_PROTECTION",
                requested_id_object=requested_id_object,
                request_user=request_user.id,
                reason="IDOR_ATTEMP_BLOCK",
            )
