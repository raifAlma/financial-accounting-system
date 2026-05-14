from fastapi import APIRouter

from .views import router as budget_router


router = APIRouter(tags=["Budget"])
router.include_router(budget_router)
