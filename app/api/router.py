from fastapi import APIRouter

from app.api.routes import auth
from app.api.routes import user
from app.api.routes import role
# from app.api.routes import media

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(role.router, prefix="/role", tags=["role"])
# api_router.include_router(media.router, prefix="/media", tags=["media"])