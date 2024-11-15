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
    return {"message": "User deleted successfully."}, 200

# TODO: Add reset password feature
