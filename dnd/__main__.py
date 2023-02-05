import asyncio
import logging

from hypercorn.asyncio import serve
from hypercorn.config import Config

from dnd.app import create_app
from dnd.settings import settings

logger = logging.getLogger(__name__)

config = Config()
config.workers = settings.WORKERS
config.debug = settings.DEBUG
config.bind = settings.BIND
config.accesslog = logger

asyncio.run(serve(create_app(), config, mode="asgi"))
