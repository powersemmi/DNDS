from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from dnd.database.db import get_db
from dnd.database.models.users import User
from dnd.models import auth
from dnd.models.auth import TokenDataModel
from dnd.utils.crypto import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/token")


async def authenticate_user(
    session: AsyncSession, username: str, password: str
):
    user = await User.get_by_username(session, username=username)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
    hasher: Hasher = Depends(Hasher),
) -> auth.UserInfoModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if payload := hasher.decode_jwt(token=token):
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataModel(username=username)
    else:
        raise credentials_exception
    user = await User.get_by_username(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return auth.UserInfoModel.from_orm(user)
