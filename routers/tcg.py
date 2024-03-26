from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import ORJSONResponse

from repo import Repo
from internal import security
from models import User, CardName, PlayerName


router = APIRouter(
    prefix="/tcg",
    tags=["tcg"]
)

user_dependency = Depends(security.get_user)


@router.get("/all", response_class=ORJSONResponse)
async def get_all_card_data(user: User = user_dependency):
    if not security.has_access(user, "tcg-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        all_cards = repo.get_tcg_table()

    return ORJSONResponse(all_cards)


@router.get("/all/cached")
async def get_all_card_data_from_cache(request: Request, user: User = user_dependency):
    if not security.has_access(user, "tcg-public"):
        raise HTTPException(status_code=401, detail="No permission")

    return request.app.tcg_cache


@router.get("/name")
async def get_card_name_from_id(id_number: int, user: User = user_dependency) -> CardName:
    if not security.has_access(user, "tcg-public"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        result = repo.get_card_name_from_id(id_number)

    if result:
        return result
    else:
        raise HTTPException(status_code=204, detail="Card ID not found.")


@router.get("/player")
async def get_player_name_from_card_id(id_number: int, user: User = user_dependency) -> PlayerName:
    if not security.has_access(user, "tcg-private"):
        raise HTTPException(status_code=401, detail="No permission")
    if not security.has_access(user, "id-name-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        owner_id = repo.get_owner_id_from_card_id(id_number)

    if not owner_id:
        raise HTTPException(status_code=204, detail="Card ID not found.")

    with Repo() as repo:
        owner_name_and_id = repo.get_player_name_from_id(owner_id)

    if owner_name_and_id:
        return PlayerName(id=id_number, name=owner_name_and_id.name)
    else:
        raise HTTPException(status_code=204, detail="Player ID not found.")


@router.get("/cards/player")
async def get_card_collection_by_player_name(player_name: str, user: User = user_dependency):
    if not security.has_access(user, "tcg-public"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        result = repo.get_collection_from_player_name(player_name)

    if result:
        return result
    else:
        raise HTTPException(status_code=204, detail="Player not found.")
