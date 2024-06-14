from fastapi import APIRouter, Depends, HTTPException
from collections import Counter

from repo import Repo
from internal import security
from models import User


router = APIRouter(
    prefix="/onelife",
    tags=["onelife"]
)

user_dependency = Depends(security.get_user)


@router.get("/user-deaths")
async def get_death_count_per_user(user: User = user_dependency) -> dict[str, int]:
    if not security.has_access(user, "onelife-public"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        names = repo.get_deaths_usernames()

    if names:
        counter = Counter(names)
        return counter
    else:
        raise HTTPException(status_code=204)
