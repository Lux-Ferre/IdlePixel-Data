import shortuuid

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from internal import security
from models import User, Paste

router = APIRouter(
    prefix="/paste",
    tags=["paste"]
)

user_dependency = Depends(security.get_user)
templates = Jinja2Templates(directory="templates")


@router.post("/")
async def new_paste(request: Request, paste: Paste, user: User = user_dependency) -> str:
    if not security.has_access(user, "paste"):
        raise HTTPException(status_code=401, detail="No permission.")
    paste_uuid = shortuuid.uuid()
    paste_data = {
        "paste": paste.paste,
        "title": paste.title,
        "creation_time": datetime.now(timezone.utc),
    }
    request.app.pastes.add_entry(paste_uuid, paste_data)
    return paste_uuid


@router.get("/", response_class=HTMLResponse)
async def get_paste(request: Request, paste_id: str):
    paste_data = request.app.pastes.get_entry(paste_id)
    if not paste_data:
        raise HTTPException(status_code=404, detail="No paste found for given ID")

    if not paste_data["title"]:
        paste_data["title"] = "Untitled Paste"

    creation_timestamp = paste_data["creation_time"].timestamp()

    return templates.TemplateResponse(
        request=request,
        name="paste.html",
        context={
            "paste_string": paste_data["paste"],
            "title": paste_data["title"],
            "creation_timestamp": creation_timestamp
        }
    )
