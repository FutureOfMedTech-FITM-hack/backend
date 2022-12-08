from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from med_backend.auth.crud import get_users
from med_backend.auth.schemas import User
from med_backend.auth.services import get_current_active_user
from med_backend.db.dependencies import get_db_session
from med_backend.users.schemas import ListUser

router = APIRouter()


@router.get("/list", response_model=list[ListUser])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
):
    if not current_user.is_manager:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to access this info",
        )
    users = await get_users(session, skip, limit)
    return users
