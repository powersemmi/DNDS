import logging.config
from pathlib import Path

import yaml
from pydantic import BaseSettings, validator
from sqlalchemy.engine import make_url

from dnd.utils.types import AsyncPostgresDsn


class Settings(BaseSettings):
    # SERVICE
    BIND: str = "0.0.0.0:8080"
    DEBUG: bool = False
    WORKERS: int = 1
    ROOT_PATH: str = "/api/v1"

    # DB
    DB_URL: AsyncPostgresDsn

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10000
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = (
        "2957d541514c6f37a84656de922e898dec4feee2607a60427dd69ec6078b8862"
    )

    # logging
    LOGGING_FILE: Path = "./logging.yaml"

    # storages
    IMAGE_DIR: Path = Path("./tmp/maps")
    GLOSSARY_DIR: Path = Path("./glossary")

    @classmethod
    @validator("DB_URL", always=True)
    def set_driver_name(cls, val):
        return str(make_url(val).set(drivername="postgresql+asyncpg"))


settings = Settings()

settings.GLOSSARY_DIR.mkdir(parents=True, exist_ok=True)
settings.IMAGE_DIR.mkdir(parents=True, exist_ok=True)

with open(settings.LOGGING_FILE, "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

logging.config.dictConfig(config)
