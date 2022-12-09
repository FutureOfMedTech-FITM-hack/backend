from pydantic import BaseModel

from med_backend.auth.schemas import UserPublicInfo


class BasePost(BaseModel):
    name: str


class PostCreate(BasePost):
    description: str


class PostList(BasePost):
    id: int

    class Config:
        orm_mode = True


class Post(BasePost):
    id: int
    description: str
    user: UserPublicInfo

    class Config:
        orm_mode = True
