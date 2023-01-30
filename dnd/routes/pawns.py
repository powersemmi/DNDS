from fastapi import APIRouter, Depends, HTTPException
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from dnd.database.db import get_db
from dnd.database.models.gamesets import GameSet
from dnd.database.models.maps import Map
from dnd.database.models.pawns import Pawn, PawnMeta
from dnd.database.models.users import User
from dnd.models.pawn import PawnMetaRequestModel, PawnModel, PawnMoveModel
from dnd.procedures.auth import check_user
from dnd.procedures.gameset import get_current_gameset

router = APIRouter(prefix="/pawn", tags=["game", "pawn"])


@router.put(
    "/{gameset_short_url}/{map_name}/{pawn_name}",
    response_model=PawnModel,
    status_code=201,
)
async def create_pawn(
    map_name: constr(max_length=30),
    pawn_name: constr(max_length=30),
    pawn_meta: PawnMetaRequestModel,
    gameset: GameSet = Depends(get_current_gameset),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
):
    gameset_map = await Map.get_by_name_and_gameset_id(
        session=session, name=map_name, gameset_id=gameset.id
    )
    exist_pawn = await Pawn.get_by_name_and_map_id(
        session=session, map_id=gameset_map.id, name=pawn_name
    )
    if exist_pawn:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    new_pawn = await Pawn.create(
        session=session, map_id=gameset_map.id, user_id=user.id, name=pawn_name
    )
    new_pawn_meta = await PawnMeta.create(
        session=session,
        pawn_id=new_pawn.id,
        color=pawn_meta.color.as_hex(),
    )
    new_pawn.meta = new_pawn_meta
    await session.commit()
    return PawnModel.from_orm(new_pawn)


@router.patch(
    "/{gameset_short_url}/{map_name}/{pawn_name}",
    response_model=PawnModel,
    status_code=201,
)
async def move_pawn(
    map_name: constr(max_length=30),
    pawn_name: constr(max_length=30),
    pawn_move: PawnMoveModel,
    gameset: GameSet = Depends(get_current_gameset),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
):
    if user:
        gameset_map = await Map.get_by_name_and_gameset_id(
            session=session, name=map_name, gameset_id=gameset.id
        )
        pawn = await Pawn.get_by_name_and_map_id(
            session=session, map_id=gameset_map.id, name=pawn_name
        )
        pawn.meta.x = pawn.meta.x if pawn.meta.x < 0 else 0
        pawn.meta.x = (
            pawn_move.x
            if pawn_move.x <= gameset_map.meta.len_x
            else gameset_map.meta.len_x
        )
        pawn.meta.y = pawn.meta.y if pawn.meta.y < 0 else 0
        pawn.meta.y = (
            pawn_move.y
            if pawn_move.y <= gameset_map.meta.len_y
            else gameset_map.meta.len_y
        )
        await session.commit()
        pawn.meta.color = pawn.meta.color.get_hex()
        return PawnModel.from_orm(pawn)
