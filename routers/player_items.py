from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from repo import Repo
from internal import security
from models import User, PlayerItems


router = APIRouter(
    prefix="/items",
    tags=["items"]
)

user_dependency = Depends(security.get_user)


@router.get("/list/name", response_class=ORJSONResponse)
async def get_specific_items_from_player_name(player_name: str, req_items: list[str], user: User = user_dependency) -> PlayerItems:
    if not security.has_access(user, "items-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        items = repo.get_specific_items_from_player_name(player_name, req_items)

    return items


@router.get("/list/id", response_class=ORJSONResponse)
async def get_specific_items_from_player_id(player_id: int, req_items: list[str], user: User = user_dependency) -> PlayerItems:
    if not security.has_access(user, "items-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        items = repo.get_specific_items_from_player_id(player_id, req_items)

    return items


@router.get("/all/name", response_class=ORJSONResponse)
async def get_all_items_from_name(player_name: str, user: User = user_dependency) -> PlayerItems:
    if not security.has_access(user, "items-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        items = repo.get_items_from_player_name(player_name)

    return items


@router.get("/all/id", response_class=ORJSONResponse)
async def get_all_items_from_id(player_id: int, user: User = user_dependency) -> PlayerItems:
    if not security.has_access(user, "items-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        items = repo.get_items_from_player_id(player_id)

    return items
