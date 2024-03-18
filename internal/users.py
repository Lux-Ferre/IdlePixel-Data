import json


class Users:
    @staticmethod
    def get_users() -> dict:
        with open("internal/users.json", mode="r", encoding="utf-8") as f:
            users = json.loads(f.read())

        return users
