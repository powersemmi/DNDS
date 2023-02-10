from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession

from dnd.database.db import get_db
from dnd.database.schemas.game_sets import GameSet
from dnd.database.schemas.pawns import Pawn, PawnMeta
from dnd.database.schemas.users import User
from dnd.models.pawn import PawnMetaRequestModel, PawnModel, PawnMoveModel
from dnd.procedures.auth import check_user
from dnd.procedures.game_set import get_current_game_set

router = APIRouter(prefix="/pawn", tags=["pawn"])


@router.get(
    "/{game_set_short_url}/{pawn_name}",
    response_model=PawnModel,
    status_code=200,
)
async def get_pawn(
    pawn_name: constr(max_length=30),
    game_set: GameSet = Depends(get_current_game_set),
    _: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
):
    pawn = await Pawn.get_by_name_and_game_set_id(
        session=session, game_set_id=game_set.id, name=pawn_name
    )
    if not pawn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put(
    "/{game_set_short_url}/{pawn_name}",
    response_model=PawnModel,
    status_code=201,
)
async def create_pawn(
    pawn_name: constr(max_length=30),
    pawn_meta: PawnMetaRequestModel,
    game_set: GameSet = Depends(get_current_game_set),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
):
    exist_pawn = await Pawn.get_by_name_and_game_set_id(
        session=session, game_set_id=game_set.id, name=pawn_name
    )
    if exist_pawn:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    new_pawn = await Pawn.create(
        session=session,
        game_set_id=game_set.id,
        user_id=user.id,
        name=pawn_name,
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
    "/{game_set_short_url}/{pawn_name}",
    response_model=PawnModel,
    status_code=201,
)
async def move_pawn(
    pawn_name: constr(max_length=30),
    pawn_move: PawnMoveModel,
    game_set: GameSet = Depends(get_current_game_set),
    _: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
):
    map_meta = game_set.meta.map
    pawn = await Pawn.get_by_name_and_game_set_id(
        session=session, game_set_id=game_set.id, name=pawn_name
    )
    if (
        pawn_move.x <= map_meta.meta.len_x
        and pawn_move.x <= map_meta.meta.len_x
    ):
        pawn.meta.x = pawn_move.x
        pawn.meta.y = pawn.meta.y
        await session.commit()
        pawn.meta.color = pawn.meta.color.get_hex()
        return PawnModel.from_orm(pawn)
    return PawnModel.from_orm(pawn)


@router.delete(
    "/{game_set_short_url}/{pawn_name}",
    response_model=PawnModel,
)
async def delete_pawn(
    pawn_name: constr(max_length=30),
    game_set: GameSet = Depends(get_current_game_set),
    _: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
):
    pawn = await Pawn.get_by_name_and_game_set_id(
        session=session, game_set_id=game_set.id, name=pawn_name
    )
    if pawn:
        await session.delete(pawn)
        await session.commit()

        return PawnModel.from_orm(pawn)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
