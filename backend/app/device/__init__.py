from flask import Blueprint

bp = Blueprint("device", __name__, url_prefix="/device")

from . import routes
