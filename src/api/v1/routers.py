from fastapi import APIRouter

from api.v1.auth import routers as auth_router
from api.v1.user.routers import user_router

router = APIRouter(prefix="/api/v1")

router.include_router(user_router, tags=["Users"])
router.include_router(auth_router.router)
