from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from api.v1.auth.dependencies import get_current_user
from infrastructure.database.postgresql.models import User
from usecases.transaction.create_transaction.abstract import (
    AbstractCreateTransactionUseCase,
)
from usecases.transaction.create_transaction.abstract import (
    AbstractCreateTransactionUseCase,
)
from usecases.transaction.get_expenses.abstract import AbstractGetExpensesUseCase
from usecases.transaction.get_list_transaction.abstract import (
    AbstractGetListTransactionUseCase,
)
from usecases.transaction.get_transaction.abstract import AbstractGetTransactionUseCase

from .dependencies import (
    create_transaction_use_case,
    get_list_transaction_use_case,
    get_transaction_use_case, get_expenses_use_case
)
from .schemas import CreateTransactionSchema, TransactionResponseSchema, TransactionFilters

router = APIRouter(prefix="/transaction")


from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: CreateTransactionSchema,
    usecase: AbstractCreateTransactionUseCase = Depends(create_transaction_use_case),
    current_user: User = Depends(get_current_user)
):
    transaction_data, warning = await usecase.execute(current_user.id, payload)
    response = transaction_data.model_dump()
    if warning:
        response["warning"] = warning
    return JSONResponse(content=jsonable_encoder(response), status_code=201)

@router.get("/{account_id}", response_model=list[TransactionResponseSchema])
async def get_transactions(
    account_id: int,
    current_user: User = Depends(get_current_user),
    filters: TransactionFilters = Depends(),
    usecase: AbstractGetListTransactionUseCase = Depends(get_list_transaction_use_case)
):
    return await usecase.execute(current_user.id, account_id, filters)

@router.get("{transaction_id}", response_model=TransactionResponseSchema)
async def get_transaction(
        transaction_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetTransactionUseCase = Depends(get_transaction_use_case)
):
    category = await usecase.execute(current_user.id, transaction_id)
    return category

@router.get("")
async def get_expenses(
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetExpensesUseCase = Depends(get_expenses_use_case),
        month: str = Query(..., description="YYYY-MM"),
):
    return await usecase.execute(current_user.id, month)
