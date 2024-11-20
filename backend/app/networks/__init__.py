from flask import Blueprint

bp = Blueprint("networks", __name__, url_prefix="/networks")

from . import routes
