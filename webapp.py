from fastapi import FastAPI

from routers import tcg, admin


app = FastAPI(
    responses={
        204: {"description": "Request is valid but no matching content found."},
        404: {"description": "Not found"},
    }
)

app.include_router(tcg.router)
app.include_router(admin.router)
