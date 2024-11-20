from flask import Blueprint

bp = Blueprint("profile", __name__, url_prefix="/me")

from . import routes
