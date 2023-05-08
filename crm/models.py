import os
from logging import getLogger

import peewee
from dotenv import load_dotenv

logger = getLogger("crm_api")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
status = load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
if not status:
    logger.error("Cannot load .env file in models file")
    raise RuntimeError("Cannot load .env file in models file")

pg_db = peewee.PostgresqlDatabase(
    database=os.environ.get("POSTGRESQL_DB_NAME"),
    user=os.environ.get("POSTGRESQL_DB_USER"),
    password=os.environ.get("POSTGRESQL_DB_PASSWD"),
    host=os.environ.get("POSTGRESQL_DB_HOST"),
    port=os.environ.get("POSTGRESQL_DB_PORT"),
    autorollback=True,
)

pg_db.connect(reuse_if_open=True)


class User(peewee.Model):
    id = peewee.AutoField()
    birthdate = peewee.DateField()
    name = peewee.TextField()
    last_name = peewee.TextField()
    email = peewee.TextField()
    password = peewee.TextField()

    class Meta:
        database = pg_db


class Role(peewee.Model):
    id = peewee.AutoField()
    role_name = peewee.TextField()
    description = peewee.TextField(null=True)

    class Meta:
        database = pg_db


class UserRoles(peewee.Model):
    user = peewee.ForeignKeyField(User, related_name="roles")
    role = peewee.ForeignKeyField(Role, related_name="users")

    class Meta:
        database = pg_db


class Products(peewee.Model):
    id = peewee.AutoField()
    name = peewee.DateField()
    quantity = peewee.TextField()
    price = peewee.BooleanField()
    category = peewee.TextField()

    class Meta:
        database = pg_db
