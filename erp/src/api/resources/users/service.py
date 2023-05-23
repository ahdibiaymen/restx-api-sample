import datetime

from flask import current_app, request
from flask_jwt_extended import create_access_token
from src import exceptions
from src.models import Role, User


class UserService:
    @classmethod
    def get_request_ip(cls):
        if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
            request_ip = request.environ["REMOTE_ADDR"]
        else:
            request_ip = request.environ["HTTP_X_FORWARDED_FOR"]
        return request_ip

    @classmethod
    def create_new_user(cls, user_info):
        """create new user instance"""
        try:
            user = User.create_new_user(user_info)
        except ValueError:
            raise exceptions.ParameterError(
                user_info=user_info, operation="CREATE_NEW_USER"
            )
        return user

    @classmethod
    def log_in_user(cls, user_info):
        """get fresh jwt token for an existing user"""

        user = User.login_user(user_info["email"], user_info["password"])
        if not user:
            raise exceptions.NotFound(
                action="LOG_IN_USER", user_email=user_info["email"]
            )

        expire_after = datetime.timedelta(
            hours=current_app.config["JWT_EXPIRE_HOURS"],
            minutes=current_app.config["JWT_EXPIRE_MINUTES"],
            seconds=current_app.config["JWT_EXPIRE_SECONDS"],
        )
        jwt_token = create_access_token(
            identity={"user_id": user.id}, expires_delta=expire_after
        )
        return user.id, jwt_token

    @classmethod
    def load_user_privileges(cls, user_id):
        """load user roles"""
        user = User.get_user_by_id(user_id)
        user_roles = user.get_user_roles()
        return {"user_id": user.id, "user_roles": user_roles}

    @classmethod
    def grant_new_privileges(cls, user_id, roles):
        """Grant new roles to a user"""
        user = User.get_user_by_id(user_id)
        all_existing_roles = Role.get_all_roles()

        for role in roles:
            if role in all_existing_roles:
                status = user.add_new_role(role)
                if not status:
                    raise exceptions.DBError(
                        user=user_id, role=role, reason="GRANT_NEW_PRIVILEGES"
                    )
            else:
                raise exceptions.NotFound(
                    action="GRANT_NEW_PRIVILEGES",
                    user_id=user_id,
                    role=role,
                    reason="ROLE_DOES_NOT_EXIST",
                )

    @classmethod
    def delete_user_privileges(cls, user_id, roles):
        """delete user roles"""
        user = User.get_user_by_id(user_id)
        if not user:
            raise exceptions.NotFound(
                action="DELETE_USER_PRIVILEGES",
                user_id=user_id,
                reason="USER_DOES_NOT_EXIST",
            )

        all_existing_roles = Role.get_all_roles()

        for role in roles:
            if role in all_existing_roles:
                status = user.remove_user_role(role)
                if not status:
                    raise exceptions.NoOperation
            else:
                raise exceptions.NotFound(
                    action="DELETE_USER_PRIVILEGES",
                    user_id=user_id,
                    role=role,
                    reason="ROLE_DOES_NOT_EXIST",
                )
