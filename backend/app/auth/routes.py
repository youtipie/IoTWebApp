from flask import request
from flask_jwt_extended import create_access_token, jwt_required, \
    create_refresh_token, get_jwt_identity

from . import bp
from .. import db
from .models import User
from ..networks.models import Network, UserNetwork
from ..utils import with_validation
from ..constants import RIGHTS


@bp.route("/register", methods=["POST"])
@with_validation({"username": str, "email": str, "password": str})
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return {"message": "User with such username or email already exists."}, 409

    try:
        new_user = User(username=username, email=email, password=password)
        new_network = Network(name="Default network")
        user_network_association = UserNetwork(
            user=new_user,
            network=new_network,
            rights=RIGHTS["a"]["code"]
        )

        db.session.add(user_network_association)
        db.session.add(new_network)
        db.session.add(new_user)
        db.session.commit()
    except ValueError as e:
        return {"message": str(e)}, 400

    return new_user.to_dict(), 201


@bp.route("/login", methods=["POST"])
@with_validation({"email": str, "password": str})
def login():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"message": "Invalid email or password."}, 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token}, 200


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token": access_token}, 200


@bp.route("/verification", methods=["POST"])
def verify_registration():
    # TODO: Email verification
    pass
