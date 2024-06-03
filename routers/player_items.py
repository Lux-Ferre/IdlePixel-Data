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


@router.get("/all", response_class=ORJSONResponse)
async def get_all_items_from_name(player_name: str, user: User = user_dependency) -> PlayerItems:
    if not security.has_access(user, "items-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        items = repo.get_items_from_player_name(player_name)

    return items
