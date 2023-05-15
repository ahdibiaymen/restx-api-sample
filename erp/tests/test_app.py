import peewee

from ..default_config import DefaultConfig
from ..models import Role
from ..security_utils import hash_and_salt_password, verify_password


def test_app_healthiness(client):
    resp = client.get(DefaultConfig.PREFIX_PATH)
    assert resp.status_code == 200


def test_database_connexion(client):
    pg_db = peewee.PostgresqlDatabase(
        database=client.application.config.get("POSTGRESQL_DB_NAME"),
        user=client.application.config.get("POSTGRESQL_DB_USER"),
        password=client.application.config.get("POSTGRESQL_DB_PASSWD"),
        host=client.application.config.get("POSTGRESQL_DB_HOST"),
        port=client.application.config.get("POSTGRESQL_DB_PORT"),
        autorollback=True,
    )
    pg_db.connect(reuse_if_open=True)


def test_app_password_verification_scheme(client):
    somepassword = "aymen"
    expected_db_hash = hash_and_salt_password(somepassword)
    assert verify_password(somepassword, expected_db_hash) == True


def test_app_roles(client):
    roles = set(Role.get_all_roles())
    desired_roles = set(["webshop-admin", "webshop-client", "reseller"])
    assert desired_roles <= roles
