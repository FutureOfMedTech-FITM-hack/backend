from pydantic import EmailStr

from med_backend.auth.schemas import UserBase


class ExtendedUser(UserBase):
    id: int
    fullname: str
    age: int


class ListUser(ExtendedUser):
    latest_form_result: str

    class Config:
        orm_mode = True


class FullUser(ListUser):
    gender: str
    email: EmailStr

    class Config:
        orm_mode = True
