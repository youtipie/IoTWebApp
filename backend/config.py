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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES") or 60))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 30)))
