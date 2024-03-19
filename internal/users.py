import json

from models import User


class Users:
    @staticmethod
    def get_users() -> list[User]:
        with open("internal/users.json", mode="r", encoding="utf-8") as f:
            users = json.loads(f.read())

        parsed_users = []

        for uuid, user_data in users.items():
            parsed_users.append(User(uuid=uuid, username=user_data["username"], permissions=user_data["permissions"]))

        return parsed_users
