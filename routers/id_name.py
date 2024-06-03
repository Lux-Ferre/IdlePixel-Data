from fastapi import APIRouter, Depends, HTTPException

from repo import Repo
from internal import security
from models import User, PlayerName


router = APIRouter(
    prefix="/id_name",
    tags=["id_name"]
)

user_dependency = Depends(security.get_user)


@router.get("/name")
async def get_player_name_from_id(player_id: int, user: User = user_dependency) -> PlayerName:
    if not security.has_access(user, "id-name-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        player_name_and_id = repo.get_player_name_from_id(player_id)

    if player_name_and_id:
        return player_name_and_id
    else:
        raise HTTPException(status_code=204, detail="Player ID not found.")


@router.get("/id")
async def get_player_id_from_name(player_name: str, user: User = user_dependency) -> PlayerName:
    if not security.has_access(user, "id-name-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        player_name_and_id = repo.get_id_from_player_name(player_name)

    if player_name_and_id:
        return player_name_and_id
    else:
        raise HTTPException(status_code=204, detail="Player ID not found.")
