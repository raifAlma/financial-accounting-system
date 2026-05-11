from fastapi import APIRouter

from .views import router as account_router


router = APIRouter(tags=["Accounts"])
router.include_router(account_router)
