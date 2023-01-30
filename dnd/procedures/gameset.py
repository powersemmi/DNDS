import logging

from fastapi import Depends, HTTPException
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from dnd.database.db import get_db
from dnd.database.models.gamesets import GameSet
from dnd.models.auth import UserInfoModel
from dnd.procedures.auth import get_current_user

logger = logging.getLogger(__name__)


async def get_current_gameset(
    gameset_short_url: constr(max_length=255),
    current_user: UserInfoModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> GameSet:
    gameset = await GameSet.get_by_short_url(
        session=session, short_url=gameset_short_url
    )
    if not gameset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GameSet not found",
        )
    logger.info(f"{current_user=} get {gameset=} with {gameset.id}")
    return gameset
