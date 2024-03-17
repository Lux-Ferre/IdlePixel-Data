from fastapi import FastAPI, Depends, HTTPException

from internal import security

app = FastAPI(
    responses={
        204: {"description": "Request is valid but no matching content found."},
        404: {"description": "Not found"},
    }
)


@app.get("/tcg-public")
async def get_test_route(user: dict = Depends(security.get_user)):
    if not security.has_access(user, "tcg-public"):
        raise HTTPException(status_code=401, detail="No permission")
    return user


@app.get("/tcg-private")
async def get_test_route(user: dict = Depends(security.get_user)):
    if not security.has_access(user, "tcg-private"):
        raise HTTPException(status_code=401, detail="No permission")
    return user
