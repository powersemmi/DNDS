from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from dnd.routes import game_sets, health, login, maps, pawns, register, users
from dnd.settings import settings
from dnd.storages.images import images

SERVICE_NAME = "DND Viewer"
API_VERSION = "0.0.1"

origins = ["*"]


def create_app():
    app = FastAPI(
        debug=settings.DEBUG,
        title=SERVICE_NAME,
        version=API_VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    v1 = "/api/v1"
    app.mount("/storge/maps", images, name="maps")
    app.include_router(health.router)
    app.include_router(register.router, prefix=v1)
    app.include_router(login.router, prefix=v1)
    app.include_router(users.router, prefix=v1)
    app.include_router(game_sets.router, prefix=v1)
    app.include_router(maps.router, prefix=v1)
    app.include_router(pawns.router, prefix=v1)
    return app
