from fastapi.staticfiles import StaticFiles

from dnd.settings import settings

images = StaticFiles(directory=settings.IMAGE_DIR)
