from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from med_backend.auth.crud import create_user
from med_backend.auth.schemas import Token, User, UserCreate, UserLogin, UserPublicInfo
from med_backend.auth.services import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from med_backend.db.dependencies import get_db_session

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    data: UserLogin,
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, str]:
    user = await authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=UserPublicInfo)
async def create_user_view(
    data: UserCreate,
    db: AsyncSession = Depends(get_db_session),
) -> User:
    user = await create_user(db, data)
    return user


@router.get("/me", response_model=UserPublicInfo)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> User:
    return current_user
