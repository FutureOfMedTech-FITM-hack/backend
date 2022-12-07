from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserBase(BaseModel):
    username: str


class UserLogin(UserBase):
    password: str


class UserCreate(UserBase):
    password: str
    email: EmailStr
    fullname: str


class UserPublicInfo(UserBase):
    id: int
    email: EmailStr
    fullname: str | None
    disabled: bool

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    email: EmailStr
    fullname: str | None
    hashed_password: str
    disabled: bool

    class Config:
        orm_mode = True
