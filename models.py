import threading

from pydantic import BaseModel
from datetime import datetime


# Util Classes
class ExpiringDict:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def add_entry(self, key, value, ttl=300):
        with self.lock:
            self.data[key] = value
            print(f"Added entry: {key} -> {value}")
            threading.Timer(ttl, self.remove_entry, args=[key]).start()

    def remove_entry(self, key):
        with self.lock:
            if key in self.data:
                print(f"Removing entry: {key}")
                del self.data[key]

    def get_entry(self, key):
        with self.lock:
            return self.data.get(key, None)


# Paste
class Paste(BaseModel):
    paste: str
    title: str = ""


# Admin
class User(BaseModel):
    uuid: str = "*****"
    username: str = "*****"
    permissions: list[str] = ["*****"]
    api_key: str = "*****"


class NewUserPermission(BaseModel):
    uuid: str
    permission: str
    allow_admin: bool = False


class NewUser(BaseModel):
    username: str
    permissions: list[str | None]
    allow_admin: bool = False


class UpdatedUser(BaseModel):
    uuid: str
    username: str
    allow_admin: bool = False


# Repo
class TCGTableRow(BaseModel):
    datetime: datetime
    holo: bool
    id: int
    name: str
    player_id: int


# TCG
class CardName(BaseModel):
    id: int
    name: str


# Player ID
class PlayerName(BaseModel):
    id: int
    name: str
