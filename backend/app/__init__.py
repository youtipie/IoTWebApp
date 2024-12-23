from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .docs import spec

db = SQLAlchemy()
jwt = JWTManager()
swagger = Swagger(template=spec)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["SWAGGER"] = {
        "openapi": "3.0.3"
    }
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

    app.db = db

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .device import bp as device_bp
    app.register_blueprint(device_bp)

    from .networks import bp as networks_bp
    app.register_blueprint(networks_bp)

    from .profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    with app.app_context():
        db.create_all()

    return app


def create_test_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["SWAGGER"] = {
        "openapi": "3.0.3"
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

    app.db = db

    from backend.app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from backend.app.device import bp as device_bp
    app.register_blueprint(device_bp)

    from backend.app.networks import bp as networks_bp
    app.register_blueprint(networks_bp)

    from backend.app.profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    with app.app_context():
        db.create_all()

    return app


from .auth import models
from .device import models
from .networks import models
