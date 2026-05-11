from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from api.v1.auth.dependencies import get_current_user
from infrastructure.database.postgresql.models import User
from usecases.transaction.create_transaction.abstract import (
    AbstractCreateTransactionUseCase,
)

from .dependencies import create_transaction_use_case, get_transaction_unit_of_work
from .schemas import CreateTransactionSchema, TransactionResponseSchema


router = APIRouter(prefix="/transaction")


@router.post(
    "", response_model=TransactionResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    payload: CreateTransactionSchema,
    usecase: AbstractCreateTransactionUseCase = Depends(create_transaction_use_case),
    current_user: User = Depends(get_current_user),
):
    transaction = await usecase.execute(current_user.id, payload)
    return transaction
