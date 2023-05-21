import hashlib

from src.default_config import DefaultConfig


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
