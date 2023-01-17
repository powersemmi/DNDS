from pydantic import BaseModel, EmailStr, constr


class UserModel(BaseModel):
    username: constr(min_length=1, max_length=256)
    email: str
    full_name: constr(min_length=1, max_length=256) | None


class UserInfoModel(UserModel):
    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class TokenDataModel(BaseModel):
    username: str | None = None


class NewUserModel(BaseModel):
    email: EmailStr
    username: constr(min_length=1, max_length=256)
    full_name: constr(min_length=1, max_length=256) | None
    password: constr(min_length=1, max_length=256)
