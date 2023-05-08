import os
from logging.config import dictConfig

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")
status = load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
if not status:
    raise RuntimeError("Cannot load .env config")


class DefaultConfig:
    PREFIX_PATH = "/api/{}".format(os.environ.get("DEPLOYMENT_VERSION"))
    DEBUG = os.environ.get("DEBUG")
    BUNDLE_ERRORS = True

    # database
    POSTGRESQL_DB_NAME = os.environ.get("CRM_PG_DATABASE")
    POSTGRESQL_DB_USER = os.environ.get("CRM_PG_USER")
    POSTGRESQL_DB_PASSWD = os.environ.get("CRM_PG_PASSWORD")
    POSTGRESQL_DB_HOST = os.environ.get("CRM_PG_HOST")
    POSTGRESQL_DB_PORT = int(os.environ.get("CRM_PG_PORT"))

    @staticmethod
    def init_loggers():
        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": (
                        "%(levelname)s -- %(asctime)s --"
                        " %(pathname)s:%(lineno)d >  %(message)s "
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "verbose",
                },
                "file": {
                    "level": "INFO",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "/tmp/crm_api.log",
                    "mode": "a",
                    "maxBytes": 10485760,
                    "backupCount": 10,
                    "formatter": "verbose",
                },
            },
            "loggers": {
                "crm_api": {
                    "level": "DEBUG",
                    "handlers": ["console", "file"],
                },
                "flask_restx": {
                    "level": "DEBUG",
                    "handlers": ["console", "file"],
                },
            },
        }
        dictConfig(LOGGING)
