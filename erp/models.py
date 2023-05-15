import os
from logging import getLogger

import peewee
from dotenv import load_dotenv

from . import exceptions, security_utils

logger = getLogger("ERP_api")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
status = load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
if not status:
    logger.error("Cannot load .env file in models file")
    raise RuntimeError("Cannot load .env file in models file")

pg_db = peewee.PostgresqlDatabase(
    database=os.environ.get("ERP_PG_DATABASE"),
    user=os.environ.get("ERP_PG_USER"),
    password=os.environ.get("ERP_PG_PASSWORD"),
    host=os.environ.get("ERP_PG_HOST"),
    port=os.environ.get("ERP_PG_PORT"),
    autorollback=True,
)


class User(peewee.Model):
    id = peewee.AutoField()
    birthdate = peewee.DateField()
    name = peewee.TextField()
    last_name = peewee.TextField()
    email = peewee.TextField()
    password = peewee.TextField()

    class Meta:
        database = pg_db

    @classmethod
    def get_user_by_id(cls, id):
        user = User.select().where(User.id == id)
        if not user:
            raise exceptions.NotFound(user_id=id)
        return user

    @classmethod
    def check_user_exist_by_email(cls, email):
        user = User.select().where(User.email == email)
        if not user:
            return None
        return user

    @classmethod
    def login_user(cls, email, password):
        user = User.select().where(User.email == email)
        if not user:
            raise exceptions.NotFound(user_email=email)
        if not security_utils.verify_password(password, user.password):
            raise exceptions.UnauthorizedAccess(email=email, operation="LOGIN")
        return user

    @classmethod
    def create_new_user(cls, name, last_name, birth_date, email, password):
        if not all((name, last_name, birth_date, email, password)):
            raise ValueError(
                "name,last_name,birth_date,email, password are required !"
            )
        # if user already exists
        if cls.check_user_exist_by_email(email):
            raise exceptions.AlreadyExist(
                email=email, operation="CREATE_NEW_USER"
            )
        # create the new user
        hashed_pw = security_utils.hash_and_salt_password(password)
        new_user = User(
            birthdate=birth_date,
            name=name,
            last_name=last_name,
            email=email,
            password=hashed_pw,
        )
        try:
            new_user.save()
            return new_user
        except peewee.PeeweeException:
            raise exceptions.DBError(
                user_email=email, operation="CREATE_NEW_USER"
            )

    def get_user_roles(self):
        try:
            user_roles = (
                UserRoles.select(Role.role_name)
                .join(Role)
                .where(UserRoles.user == self.id)
            )

            return [role.role_name for role in user_roles]
        except peewee.PeeweeException:
            raise exceptions.DBError

    def add_new_role(self, role_name):
        try:
            if not role_name:
                raise exceptions.NotFound
            role = Role.select().where(Role.role_name == role_name).first()
            if not role:
                raise exceptions.NotFound
            # check if role already granted
            user_role = (
                UserRoles.select()
                .join(Role)
                .where(
                    (UserRoles.user == self.id) & (Role.role_name == role_name)
                )
            )
            if user_role:
                raise exceptions.AlreadyExist
            new_user_role = UserRoles(user=self, role=role)
            new_user_role.save()
            return True
        except peewee.PeeweeException:
            raise exceptions.DBError

    def remove_user_role(self, role_name):
        try:
            if not role_name:
                raise exceptions.NotFound
            user_role = (
                UserRoles.select()
                .join(Role)
                .where(
                    (Role.role_name == role_name) & (UserRoles.user == self.id)
                )
                .first()
            )
            if not user_role:
                return False
            user_role.delete_instance()
            return True
        except peewee.PeeweeException:
            raise exceptions.DBError

    def is_admin(self):
        try:
            admin_role = Role.select().where(Role.role_name == "admin").first()
            is_admin = UserRoles.select().where(
                (UserRoles.user == self.id) & (UserRoles.role == admin_role.id)
            )
            if is_admin:
                return True
            else:
                return False
        except peewee.PeeweeException:
            raise exceptions.DBError

    def has_any_role(self, *roles):
        return any(self.has_role(role) for role in roles)


class Role(peewee.Model):
    id = peewee.AutoField()
    role_name = peewee.TextField(unique=True)
    description = peewee.TextField(null=True)

    class Meta:
        database = pg_db

    @classmethod
    def init_roles(cls):
        roles = {
            "reseller": "Has access to products and stocks",
            "webshop-admin": "Has access to CRM & ERP",
            "webshop-client": (
                "Has access to all available products & his own commands"
            ),
        }
        for role_name, description in roles.items():
            role = Role.select().where(Role.role_name == role_name)
            if not role:
                try:
                    role = Role(role_name=role_name, description=description)
                    role.save()
                except peewee.PeeweeException:
                    pass

    @classmethod
    def get_all_roles(cls):
        return [role.role_name for role in Role.select()]


class UserRoles(peewee.Model):
    user = peewee.ForeignKeyField(User, related_name="roles")
    role = peewee.ForeignKeyField(Role, related_name="users")

    class Meta:
        database = pg_db


class Product(peewee.Model):
    id = peewee.AutoField()
    name = peewee.TextField()
    quantity = peewee.IntegerField()
    category = peewee.TextField()
    price = peewee.FloatField()

    class Meta:
        database = pg_db


class Order(peewee.Model):
    user = peewee.ForeignKeyField(User, related_name="products")
    product = peewee.ForeignKeyField(Role, related_name="users")
    order_id = peewee.AutoField()
    order_date = peewee.DateField()

    class Meta:
        database = pg_db


pg_db.create_tables([User, Role, Product, UserRoles, Order])
pg_db.connect(reuse_if_open=True)
