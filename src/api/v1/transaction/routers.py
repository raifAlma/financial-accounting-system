from fastapi import APIRouter

from .views import router as transaction_router


router = APIRouter(tags=["Transaction"])
router.include_router(transaction_router)
