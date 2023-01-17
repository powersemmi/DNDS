from pydantic import PostgresDsn


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {
        "postgresql",
        "postgresql+aiopg",
        "postgres",
    }
