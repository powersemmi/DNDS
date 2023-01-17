from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from dnd.routes import health, login, pawns, register, users
from dnd.settings import settings

SERVICE_NAME = "DND Viewer"
API_VERSION = "0.0.1"

origins = [
    f"http://{settings.BIND}",
    f"https://{settings.BIND}",
]


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

    app.include_router(health.router)
    app.include_router(register.router, prefix=v1)
    app.include_router(login.router, prefix=v1)
    app.include_router(users.router, prefix=v1)
    app.include_router(pawns.router, prefix=v1)
    return app
