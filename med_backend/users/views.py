from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from med_backend.auth.schemas import User
from med_backend.db.dependencies import get_db_session
from med_backend.users import crud
from med_backend.users.schemas import FullUser, ListUser
from med_backend.users.services import get_current_active_manager

router = APIRouter()


@router.get("/list", response_model=list[ListUser])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_manager),
    session: AsyncSession = Depends(get_db_session),
):
    users = await crud.get_users(session, skip, limit)
    return users


@router.get("/{key}", response_model=FullUser)
async def get_user(
    key: int,
    current_user: User = Depends(get_current_active_manager),
    session: AsyncSession = Depends(get_db_session),
):
    user = await crud.get_user(session, key)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
