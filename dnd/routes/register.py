from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from dnd.database.db import get_db
from dnd.database.models.users import User
from dnd.models import auth

router = APIRouter(prefix="/register")


class ConflictError(BaseModel):
    detail: str = "User is already exists"


class SuccessMessage(BaseModel):
    detail: str = "Created"


@router.put(
    "/",
    tags=["auth"],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": SuccessMessage},
        status.HTTP_409_CONFLICT: {"model": ConflictError},
    },
)
async def registration(
    new_user: auth.NewUserModel, session: AsyncSession = Depends(get_db)
):
    try:
        await User.create(session=session, **new_user.dict())
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already exists",
        )

    return SuccessMessage()
