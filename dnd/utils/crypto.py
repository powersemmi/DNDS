from datetime import datetime, timedelta

from hashids import Hashids
from jose import JWTError, jwt
from passlib.context import CryptContext

from dnd.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashids = Hashids(salt=settings.SECRET_KEY, min_length=6)


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: bytes) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def decode_jwt(token) -> dict | None:
        try:
            return jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            return None

    @staticmethod
    def generate_jwt(
        username: str,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    ):
        access_token_expires = datetime.utcnow() + timedelta(
            minutes=access_token_expire_minutes,
        )
        data = {"sub": username, "exp": access_token_expires}

        encoded_jwt = jwt.encode(
            data,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return encoded_jwt


async def get_shortcut():
    yield hashids
