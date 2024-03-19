from fastapi import APIRouter, Depends, HTTPException

from repo import Repo
from internal import security
from models import User, CardName, TCGTableRow


router = APIRouter(
    prefix="/tcg",
    tags=["tcg"]
)

user_dependency = Depends(security.get_user)


@router.get("/all")
async def get_all_card_data(user: User = user_dependency) -> list[TCGTableRow]:
    if not security.has_access(user, "tcg-private"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        all_cards = repo.get_tcg_table()

    return all_cards


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
