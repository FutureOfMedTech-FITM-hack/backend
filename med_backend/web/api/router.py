from fastapi.routing import APIRouter

from med_backend import auth, forms, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(forms.router, prefix="/forms", tags=["forms"])
