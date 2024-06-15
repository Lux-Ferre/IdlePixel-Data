import json

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from models import User
from internal.users import Users

api_key_header = APIKeyHeader(name="X-API-Key")


def get_user_from_api_key(api_key: str, api_keys: dict) -> User:
    user_data = Users.get_users()
    for user in user_data:
        if user.uuid == api_keys[api_key]:
            return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )


def get_user(api_key: str = Security(api_key_header)):
    with open("internal/keys.json") as key_file:
        api_keys = json.load(key_file)
    if api_key in api_keys:
        user = get_user_from_api_key(api_key, api_keys)
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )


def has_access(user: User, permission: str):
    permissions_list = [
        "admin",
        "tcg-public", "tcg-private",
        "hiscore-public", "hiscore-private",
        "one-life-public", "one-life-private",
        "id-name-private",
    ]
    return permission in user.permissions
