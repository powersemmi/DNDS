from pydantic import PostgresDsn


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {
        "postgresql",
        "postgresql+asyncpg",
        "postgres",
    }
