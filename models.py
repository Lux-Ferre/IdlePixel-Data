from pydantic import BaseModel
from datetime import datetime


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
