import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from dnd.app import create_app
from dnd.settings import settings

config = Config()
config.workers = settings.WORKERS
config.debug = settings.DEBUG
config.bind = settings.BIND

asyncio.run(serve(create_app(), config, mode="asgi"))
