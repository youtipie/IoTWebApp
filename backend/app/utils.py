import asyncio

from .auth.models import User
from flask import request
from functools import wraps
from typing import Tuple

from flask_jwt_extended import jwt_required, get_jwt_identity


def validate_user_data(data, required_fields: dict[str, type]) -> Tuple[dict[str, str], int] | bool:
    if not data:
        return {"message": f"Request body must be JSON and contain {', '.join(required_fields)}."}, 400

    for field, field_type in required_fields.items():
        if field not in data:
            return {"message": f"{field.capitalize()} is required."}, 400
        field_data = data[field]
        if not isinstance(field_data, field_type) or not str(field_data).strip():
            return {"message": f"{field.capitalize()} must be a non-empty {field_type.__name__}."}, 400

    return True


def with_validation(required_fields: dict[str, type]):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            validation = validate_user_data(request.json, required_fields)
            if validation != True:
                return validation
            return func(*args, **kwargs)

        return wrapper

    return inner


def with_auth(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User with such id does not exist."}, 404

        if asyncio.iscoroutinefunction(func):
            return asyncio.run(func(*args, user=user, **kwargs))
        else:
            return func(*args, user=user, **kwargs)

    return wrapper
