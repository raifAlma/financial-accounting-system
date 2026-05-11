from fastapi import APIRouter

from api.v1.account.routers import account_router
from api.v1.auth import routers as auth_router
from api.v1.category.routers import category_router
from api.v1.transaction.routers import transaction_router
from api.v1.user.routers import user_router


router = APIRouter(prefix="/api/v1")

router.include_router(user_router, tags=["Users"])
router.include_router(auth_router.router)
router.include_router(account_router, tags=["Accounts"])

router.include_router(transaction_router, tags=["Transactions"])
router.include_router(category_router, tags=["Categories"])
