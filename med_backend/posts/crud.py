from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from med_backend.db.models.posts import PostScheme
from med_backend.posts.schemas import PostCreate
from med_backend.users.crud import get_user


async def get_posts(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[PostScheme] | None:
    r = await session.execute(
        select(PostScheme).offset(skip).limit(limit),
    )
    posts = r.scalars().all()
    return posts


async def get_post(session: AsyncSession, post_id: int) -> PostScheme | None:
    r = await session.execute(
        select(PostScheme)
        .options(selectinload(PostScheme.user))
        .where(PostScheme.id == post_id),
    )
    post = r.scalars().first()
    return post


async def create_post(
    session: AsyncSession,
    data: PostCreate,
    user_id: int,
) -> PostScheme:
    user = await get_user(session, user_id)
    if not user or not user.is_manager:
        raise HTTPException(status_code=422, detail="User can't be used")

    obj = PostScheme(name=data.name, description=data.description, user_id=user_id)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj
