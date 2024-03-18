from fastapi import APIRouter, Depends, HTTPException

from internal import security
from models import CardName

router = APIRouter(
    prefix="/tcg",
    tags=["tcg"]
)

user_dependency = Depends(security.get_user)


@router.get("/name")
async def get_card_name_from_id(id_number: str, user: dict = user_dependency) -> CardName:
    if not security.has_access(user, "tcg-public"):
        raise HTTPException(status_code=401, detail="No permission")

    return CardName(id=id_number, name="test")
