import os
import uuid
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or str(uuid.uuid4())
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or ""
    SQLALCHEMY_TRACK_MODIFICATIONS = int(os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False))
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or str(uuid.uuid4())
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES") or 60))
    # If true this will only allow the cookies that contain your JWTs to be sent
    # over https. In production, this should always be set to True
    JWT_COOKIE_SECURE = int(os.environ.get("JWT_COOKIE_SECURE", False))
    JWT_TOKEN_LOCATION = ["cookies"]
    # Always set true in production
    JWT_COOKIE_CSRF_PROTECT = int(os.environ.get("JWT_COOKIE_CSRF_PROTECT", False))
