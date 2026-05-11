from fastapi import APIRouter

from .views import router as category_router


router = APIRouter(tags=["Category"])
router.include_router(category_router)
