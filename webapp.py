from fastapi import FastAPI

from routers import tcg

app = FastAPI(
    responses={
        204: {"description": "Request is valid but no matching content found."},
        404: {"description": "Not found"},
    }
)

app.include_router(tcg.router)
