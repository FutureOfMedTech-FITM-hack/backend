from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from med_backend.auth.schemas import User
from med_backend.auth.services import get_current_active_user
from med_backend.db.dependencies import get_db_session
from med_backend.posts import crud
from med_backend.posts.schemas import Post, PostCreate, PostList

router = APIRouter()


@router.get("/all", response_model=list[PostList])
async def get_all_posts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
):
    posts = await crud.get_posts(session, skip, limit)
    return posts


@router.get("/{post_id}", response_model=Post)
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
):
    form = await crud.get_post(session, post_id)
    return form


@router.post("/create", response_model=Post)
async def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
):
    post = await crud.create_post(session, data, current_user.id)
    return post
