from inspect import Parameter, Signature
from typing import Any, Awaitable, Callable

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from dnd.database.db import get_db

router = APIRouter(prefix="/health")


async def default_handler(**kwargs) -> dict[str, Any]:
    output = {}
    for value in kwargs.values():
        if isinstance(value, dict):
            output.update(value)
    return output


def health(
    conditions: list[Callable[..., Any | bool]],
    *,
    success_handler: Callable[..., Awaitable] = default_handler,
    failure_handler: Callable[..., Awaitable] = default_handler,
    success_status: int = 200,
    failure_status: int = 503,
):
    async def endpoint(**dependencies):
        if all(dependencies.values()):
            handler = success_handler
            status_code = success_status
        else:
            handler = failure_handler
            status_code = failure_status

        output = await handler(**dependencies)
        return JSONResponse(jsonable_encoder(output), status_code=status_code)

    params = []
    for condition in conditions:
        params.append(
            Parameter(
                f"{condition.__name__}",
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                annotation=bool,
                default=Depends(condition),
            )
        )
    endpoint.__signature__ = Signature(params)
    return endpoint


async def is_database_online(session: AsyncSession = Depends(get_db)):
    res = await session.execute(text("SELECT 1 as one"))
    res = res.one()[0]
    return {"is_database_online": "OK"} if res == 1 else False


router.add_api_route("", health([is_database_online]))
