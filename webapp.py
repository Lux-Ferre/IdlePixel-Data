from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from threading import Timer

from routers import tcg, admin, paste, id_name, player_items
from repo import Repo
from models import ExpiringDict


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def cache_next_page():
    with Repo() as repo:
        next_page = repo.cache_next_page(app.tcg_cache_page)

    if not next_page:
        app.tcg_cache_page = 0
    else:
        app.tcg_cache_page += 1
        for card in next_page:
            app.tcg_cache[card[0]] = {
                "name": card[1],
                "holo": card[2],
                "player_id": card[3],
                "datetime": card[4],
                "opened_by_id": card[5],
            }


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

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(tcg.router)
app.include_router(player_items.router)
app.include_router(id_name.router)
app.include_router(paste.router)
app.include_router(admin.router)

app.pastes = ExpiringDict()

app.tcg_cache_page = 0
app.tcg_cache = {}

tcg_rolling_cache_timer = RepeatTimer(1, cache_next_page)
tcg_rolling_cache_timer.start()
