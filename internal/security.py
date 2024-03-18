from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from internal.users import Users


api_keys = {
    "e54d4431-5dab-474e-b71a-0db1fcb9e659": "7oDYjo3d9r58EJKYi5x4E8",
    "5f0c7127-3be9-4488-b801-c7b6415b45e9": "mUP7PpTHmFAkxcQLWKMY8t"
}

api_key_header = APIKeyHeader(name="X-API-Key")


def check_api_key(api_key: str) -> bool:
    return api_key in api_keys


def get_user_from_api_key(api_key: str) -> str:
    user_data = Users.get_users()
    return user_data[api_keys[api_key]]


def get_user(api_key: str = Security(api_key_header)):
    if check_api_key(api_key):
        user = get_user_from_api_key(api_key)
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )


def has_access(user: dict, permission: str):
    return permission in user["permissions"]
