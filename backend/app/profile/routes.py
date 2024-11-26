from flask import jsonify
from flask_jwt_extended import unset_access_cookies

from . import bp
from .. import db
from ..auth.models import User

from ..utils import with_auth


@bp.route("", methods=["GET"])
@with_auth
def get_profile(user: User):
    return user.to_dict(), 200


@bp.route("", methods=["DELETE"])
@with_auth
def delete_profile(user: User):
    user.delete_user()
    db.session.commit()
    resp = jsonify({"message": "User deleted successfully."})
    unset_access_cookies(resp)
    return resp, 200

# TODO: Add reset password feature
