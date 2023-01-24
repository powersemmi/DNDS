from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnd.database.db import get_db
from dnd.models.auth import UserInfoModel
from dnd.procedures.auth import get_current_user

router = APIRouter(prefix="/gamesets")


@router.put("")
async def create_gameset(
    current_user: UserInfoModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    ...
