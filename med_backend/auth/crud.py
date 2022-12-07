from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models.users import UserScheme
from . import schemas, services
from .schemas import User


async def get_user(session: AsyncSession, username: str) -> User | None:
    r = await session.execute(select(UserScheme).where(UserScheme.username == username))
    user = r.scalars().first()
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    r = await session.execute(select(UserScheme).where(UserScheme.email == email))
    user = r.scalars().first()
    return user


async def get_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[User] | None:
    r = await session.execute(select(UserScheme).offset(skip).limit(limit))
    users = r.scalars().all()
    return users


async def create_user(session: AsyncSession, user: schemas.UserCreate) -> UserScheme:
    if await get_user(session, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    if await get_user_by_email(session, user.email):
        raise HTTPException(status_code=400, detail="Email already taken")

    hashed_password = services.get_password_hash(user.password)
    db_user = UserScheme(
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        hashed_password=hashed_password,
        disabled=False,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
