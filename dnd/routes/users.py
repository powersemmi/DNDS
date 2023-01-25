from fastapi import APIRouter, Depends

from dnd.database.models.users import User
from dnd.models.gameset import GameSetModel
from dnd.models.map import MapsModel
from dnd.procedures.auth import check_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/maps", response_model=MapsModel)
async def get_user_maps(
    user: User = Depends(check_user),
):
    return MapsModel(maps=user.maps)


@router.get("/gamesets")
async def get_user_gamesets(
    user: User = Depends(check_user),
) -> list[GameSetModel]:
    return [GameSetModel.from_orm(gameset) for gameset in user.gamesets]


@router.get("/in_games")
async def get_user_in_games(
    user: User = Depends(check_user),
) -> list[GameSetModel]:
    return [GameSetModel.from_orm(mapper.gameset) for mapper in user.in_games]
