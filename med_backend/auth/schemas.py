from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, EmailStr, root_validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserLogin(UserBase):
    password: str


class UserCreate(UserBase):
    password: str
    fullname: str
    gender: str
    born: datetime


class UserPublicInfo(UserBase):
    id: int
    fullname: str | None
    disabled: bool
    born: date

    @root_validator(pre=False)
    def _set_fields(cls, values):
        values["age"] = relativedelta(datetime.now(), values["born"]).years
        values.pop("born")
        return values

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    fullname: str
    hashed_password: str
    disabled: bool
    is_manager: bool

    class Config:
        orm_mode = True


class UpdateUserBase(UserBase):
    fullname: str


class UpdateUserProfile(UpdateUserBase):
    disabled: bool
    is_manager: bool
