from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from med_backend.auth import schemas, services
from med_backend.db.models.users import UserScheme


async def get_user_by_email(session: AsyncSession, email: str) -> schemas.User | None:
    r = await session.execute(select(UserScheme).where(UserScheme.email == email))
    user = r.scalars().first()
    return user


async def get_user(session: AsyncSession, pk: int) -> schemas.User | None:
    r = await session.execute(select(UserScheme).where(UserScheme.id == pk))
    user = r.scalars().first()
    return user


async def get_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[schemas.User] | None:
    r = await session.execute(
        select(UserScheme)
        .where(UserScheme.is_manager == False)
        .offset(skip)
        .limit(limit),
    )
    users = r.scalars().all()
    return users


async def create_user(session: AsyncSession, user: schemas.UserCreate) -> UserScheme:
    if await get_user_by_email(session, user.email):
        raise HTTPException(status_code=422, detail="Email already taken")

    hashed_password = services.get_password_hash(user.password)
    db_user = UserScheme(
        email=user.email,
        fullname=user.fullname,
        gender=user.gender,
        born=user.born.date(),
        hashed_password=hashed_password,
        disabled=False,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
