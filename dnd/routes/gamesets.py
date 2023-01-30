from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from hashids import Hashids
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession

from dnd.database.db import get_db
from dnd.database.models.gamesets import GameSet, GameSetMeta
from dnd.database.models.users import User, UserInGameset
from dnd.models.gameset import GameSetModel
from dnd.procedures.auth import check_user
from dnd.procedures.gameset import get_current_gameset
from dnd.utils.crypto import get_shortcut

router = APIRouter(prefix="/gameset", tags=["game", "gameset"])


@router.put(
    "", response_model=GameSetModel, status_code=status.HTTP_201_CREATED
)
async def create_gameset(
    name: constr(max_length=60),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
    shortcut: Hashids = Depends(get_shortcut),
) -> GameSetModel:
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


@router.get("/{gameset_short_url}/", response_model=GameSetModel)
async def get_gameset(
    user: User = Depends(check_user),
    gameset: GameSet = Depends(get_current_gameset),
):
    if (
        user.id in [user.user_id for user in gameset.users_in_game]
        or user.id == gameset.owner.id
    ):
        return GameSetModel.from_orm(gameset)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="GameSet not found",
    )


@router.put(
    "/join/{gameset_short_url}/",
    status_code=202,
    responses={
        status.HTTP_406_NOT_ACCEPTABLE: {"status": "not acceptable"},
        status.HTTP_202_ACCEPTED: {"status": "accepted"},
        status.HTTP_304_NOT_MODIFIED: {"status": "not modified"},
    },
)
async def join_to_game(
    user: User = Depends(check_user),
    gameset: GameSet = Depends(get_current_gameset),
    session: AsyncSession = Depends(get_db),
):
    if user.id == gameset.owner.id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    elif user.id in [user.user_id for user in gameset.users_in_game]:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    user_in_game = await UserInGameset.create(
        session=session, user_id=user.id, gameset_id=gameset.id
    )
    user.in_games.append(user_in_game)
    gameset.users_in_game.append(user_in_game)
    await session.commit()
    return Response(status_code=202, content="accepted")
