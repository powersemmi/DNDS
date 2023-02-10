from starlette.staticfiles import StaticFiles

from dnd.settings import settings

glossary = StaticFiles(directory=settings.GLOSSARY_DIR)
