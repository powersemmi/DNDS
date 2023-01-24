from fastapi import APIRouter, Depends
from hashids import Hashids
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession

from dnd.database.db import get_db
from dnd.database.models.gamesets import GameSet, GameSetMeta
from dnd.database.models.users import User
from dnd.models.auth import UserInfoModel
from dnd.models.gameset import GameSetModel
from dnd.procedures.auth import get_current_user
from dnd.utils.crypto import get_shortcut

router = APIRouter(prefix="/gamesets", tags=["game"])


@router.put("", response_model=GameSetModel)
async def create_gameset(
    name: constr(max_length=60),
    current_user: UserInfoModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    shortcut: Hashids = Depends(get_shortcut),
):
    user = await User.get_by_username(
        session=session, username=current_user.username
    )
    gameset_id = await GameSet.get_next_id(session=session)
    short_url = shortcut.encode(gameset_id)
    new_gameset = await GameSet.create(
        session=session,
        gameset_id=gameset_id,
        owner_id=user.id,
        name=name,
        short_url=short_url,
    )
    gameset_meta = await GameSetMeta.create(
        gameset_id=new_gameset.id,
        session=session,
    )
    new_gameset.meta = gameset_meta
    await session.commit()
    return GameSetModel.from_orm(new_gameset)
