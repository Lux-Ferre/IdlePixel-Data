import shortuuid

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse

from internal import security
from models import User, Paste

router = APIRouter(
    prefix="/paste",
    tags=["paste"]
)

user_dependency = Depends(security.get_user)


@router.post("/")
async def new_paste(request: Request, paste: Paste, user: User = user_dependency) -> str:
    if not security.has_access(user, "paste"):
        raise HTTPException(status_code=401, detail="No permission.")
    paste_uuid = shortuuid.uuid()
    request.app.pastes.add_entry(paste_uuid, paste.paste)
    return paste_uuid


@router.get("/", response_class=HTMLResponse)
async def get_paste(request: Request, paste_id: str) -> str:
    paste_string = request.app.pastes.get_entry(paste_id)
    if not paste_string:
        raise HTTPException(status_code=404, detail="No paste found for given ID")
    return f"""
    <html>
        <body>
            <textarea style="width:90vw;height:90vh;" readonly>
{paste_string}
            </textarea>
        </body>
    </html>
"""
