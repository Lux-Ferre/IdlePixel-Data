import json

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from models import User
from internal.users import Users


with open("internal/keys.json") as key_file:
    api_keys = json.load(key_file)

api_key_header = APIKeyHeader(name="X-API-Key")


def check_api_key(api_key: str) -> bool:
    return api_key in api_keys


def get_user_from_api_key(api_key: str) -> User:
    user_data = Users.get_users()
    for user in user_data:
        if user.uuid == api_keys[api_key]:
            return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )


def get_user(api_key: str = Security(api_key_header)):
    if check_api_key(api_key):
        user = get_user_from_api_key(api_key)
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )


def has_access(user: User, permission: str):
    return permission in user.permissions
