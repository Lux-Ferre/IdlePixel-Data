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
        return dict(counter.most_common())
    else:
        raise HTTPException(status_code=204)


@router.get("/levels-lost")
async def get_levels_lost_per_enemy(user: User = user_dependency):
    if not security.has_access(user, "onelife-public"):
        raise HTTPException(status_code=401, detail="No permission")

    with Repo() as repo:
        counter = repo.get_levels_lost_per_enemy()

    if counter:
        return {k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)}
    else:
        raise HTTPException(status_code=204)
