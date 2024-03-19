import json
import uuid
import shortuuid

from fastapi import APIRouter, Depends, HTTPException

from internal import security
from internal.users import Users

from models import User, NewUser, NewUserPermission


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

user_dependency = Depends(security.get_user)


@router.get("/user")
async def get_user_data(req_uuid: str = None, user: User = user_dependency) -> list[User] | User:
    if not security.has_access(user, "admin"):
        raise HTTPException(status_code=401, detail="No permission.")

    user_data = Users.get_users()

    if req_uuid is None:
        return user_data

    for stored_user in user_data:
        if stored_user.uuid == req_uuid:
            return stored_user

    raise HTTPException(status_code=204, detail="User not found.")


@router.post("/user/")
async def add_new_user(new_user: NewUser, user: User = user_dependency) -> User:
    if not security.has_access(user, "admin"):
        raise HTTPException(status_code=401, detail="No permission")

    if "admin" in new_user.permissions and not new_user.allow_admin:
        raise HTTPException(status_code=401, detail="Cannot add new admin account without allow_admin.")

    with open("internal/users.json", mode="r", encoding="utf-8") as users_file:
        users = json.load(users_file)

    for stored_user in users:
        if stored_user["username"] == new_user.username:
            raise HTTPException(status_code=409, detail="User already exists.")

    user_uuid = shortuuid.uuid()
    api_key = str(uuid.uuid4())

    with open("internal/keys.json", mode="r", encoding="utf-8") as key_file:
        api_keys = json.load(key_file)

    api_keys[api_key] = user_uuid

    with open("internal/keys.json", mode="w", encoding="utf-8") as key_file:    # Save updated keys
        json.dump(api_keys, key_file, indent=4)

    users[user_uuid] = {
        "permissions": new_user.permissions,
        "username": new_user.username
    }

    with open("internal/users.json", mode="w+", encoding="utf-8") as users_file:    # Save updated users
        json.dump(users, users_file, indent=4)

    return User(uuid=user_uuid, username=new_user.username, permissions=new_user.permissions)


@router.put("/user/perm")
async def give_user_permission(updated_user_perm: NewUserPermission, user: User = user_dependency) -> User:
    if not security.has_access(user, "admin"):
        raise HTTPException(status_code=401, detail="No permission")

    if updated_user_perm.permission == "admin" and not updated_user_perm.allow_admin:
        raise HTTPException(status_code=401, detail="Cannot add admin permission without allow_admin.")

    with open("internal/users.json", mode="r", encoding="utf-8") as users_file:
        users = json.load(users_file)

    if updated_user_perm.uuid not in users:
        raise HTTPException(status_code=204, detail="User not found.")

    if updated_user_perm.permission not in users[updated_user_perm.uuid]["permissions"]:
        users[updated_user_perm.uuid]["permissions"].append(updated_user_perm.permission)

    with open("internal/users.json", mode="w+", encoding="utf-8") as users_file:    # Save updated users
        json.dump(users, users_file, indent=4)

    return User(uuid=updated_user_perm.uuid, username=users[updated_user_perm.uuid]["username"], permissions=users[updated_user_perm.uuid]["permissions"])


@router.delete("/user/perm")
async def remove_user_permission(updated_user_perm: NewUserPermission, user: User = user_dependency) -> User:
    if not security.has_access(user, "admin"):
        raise HTTPException(status_code=401, detail="No permission")

    if updated_user_perm.permission == "admin" and not updated_user_perm.allow_admin:
        raise HTTPException(status_code=401, detail="Cannot remove admin permission without allow_admin.")

    with open("internal/users.json", mode="r", encoding="utf-8") as users_file:
        users = json.load(users_file)

    if updated_user_perm.uuid not in users:
        raise HTTPException(status_code=204, detail="User not found.")

    if updated_user_perm.permission not in users[updated_user_perm.uuid]["permissions"]:
        raise HTTPException(status_code=204, detail="User does not have permission.")

    users[updated_user_perm.uuid]["permissions"].remove(updated_user_perm.permission)

    with open("internal/users.json", mode="w+", encoding="utf-8") as users_file:    # Save updated users
        json.dump(users, users_file, indent=4)

    return User(uuid=updated_user_perm.uuid, username=users[updated_user_perm.uuid]["username"], permissions=users[updated_user_perm.uuid]["permissions"])
