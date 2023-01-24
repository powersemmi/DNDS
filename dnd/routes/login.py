from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from dnd.database.db import get_db
from dnd.models.auth import TokenModel
from dnd.procedures.auth import authenticate_user
from dnd.utils.crypto import Hasher

router = APIRouter(prefix="/login", tags=["auth"])


@router.post("/token", response_model=TokenModel)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
    hasher: Hasher = Depends(Hasher),
):
    user = await authenticate_user(
        session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = hasher.generate_jwt(username=user.username)
    return {"access_token": access_token, "token_type": "bearer"}
