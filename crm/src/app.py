from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from src import models
from src.api.routes import register_endpoints_routes
from src.default_config import DefaultConfig


def create_app():
    app = Flask(__name__)

    DefaultConfig.init_loggers()

    models.Role.init_roles()

    app.config.from_object(DefaultConfig)

    crm_api = Api(
        app,
        prefix=DefaultConfig.PREFIX_PATH,
        description="CRM API",
        doc=DefaultConfig.PREFIX_PATH,
    )

    register_endpoints_routes(crm_api)

    JWTManager(app)

    return app


if __name__ == "__main__":
    create_app().run(debug=False)
