from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import tcg, admin


app = FastAPI(
    responses={
        204: {"description": "Request is valid but no matching content found."},
        404: {"description": "Not found"},
    },
    root_path="/api"
)

origins = [
    "http://localhost",
    "http://localhost:8042",
    "https://data.idle-pixel.com/",
    "https://idle-pixel.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tcg.router)
app.include_router(admin.router)
