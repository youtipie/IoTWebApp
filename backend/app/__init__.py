from datetime import datetime, timezone, timedelta

from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, create_access_token, set_access_cookies
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
        "openapi": "3.0.1"
    }
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

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

    # Maybe move somewhere more appropriate
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            return response

    return app


from .auth import models
from .device import models
from .networks import models
