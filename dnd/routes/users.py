from fastapi import APIRouter, Depends

from dnd.models.auth import UserInfoModel, UserModel
from dnd.procedures.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UserModel)
async def read_users_me(
    current_user: UserInfoModel = Depends(get_current_user),
):
    return current_user


@router.get("/me/items/")
async def read_own_items(
    current_user: UserInfoModel = Depends(get_current_user),
):
    return [{"item_id": "Foo", "owner": current_user.username}]
