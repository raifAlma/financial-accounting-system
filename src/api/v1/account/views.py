from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from api.v1.auth.dependencies import get_current_user
from infrastructure.database.postgresql.models import User
from usecases.account.create_account.abstract import AbstractCreateAccountUseCase
from usecases.account.delete_account.abstract import AbstractDeleteAccountUseCase
from usecases.account.get_balance.abstract import AbstractGetBalanceUseCase
from usecases.account.update_account.abstract import AbstractUpdateAccountUseCase
from usecases.account.get_account.abstract import AbstractGetAccountUseCase
from usecases.account.get_list_account.abstract import AbstractGetListAccountUseCase

from .dependencies import (
    create_account_use_case,
    delete_account_use_case,
    update_account_use_case,
    get_account_use_case,
    get_list_account_use_case, get_balance_use_case
)
from .schemas import AccountResponseSchema, AccountUpdateSchema, CreateAccountSchema


router = APIRouter(prefix="/account")


@router.post(
    "", response_model=AccountResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_account(
    payload: CreateAccountSchema,
    usecase: AbstractCreateAccountUseCase = Depends(create_account_use_case),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    try:
        account = await usecase.execute(current_user.id, payload)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return account


@router.get(
    "/{account_id}", response_model=AccountResponseSchema)
async def get_account(
        account_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetAccountUseCase = Depends(get_account_use_case),
):
    account = await usecase.execute(current_user.id, account_id)
    return account

@router.get("", response_model=list[AccountResponseSchema])
async def get_list_account(
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetListAccountUseCase = Depends(get_list_account_use_case),
):
    account = await usecase.execute(current_user.id)
    return account

@router.get('', response_model=dict[str, float])
async def get_balance(
    current_user: User = Depends(get_current_user),
    usecase: AbstractGetBalanceUseCase = Depends(get_balance_use_case)
):
    return await usecase.execute(current_user.id)

@router.put("/{account_id}", response_model=AccountResponseSchema)
async def update_account(
    account_id: int,
    payload: AccountUpdateSchema,
    usecase: AbstractUpdateAccountUseCase = Depends(update_account_use_case),
    current_user: User = Depends(get_current_user),
):
    updated = await usecase.execute(current_user.id, account_id, payload)
    return updated


@router.delete("/{account_id}")
async def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    usecase: AbstractDeleteAccountUseCase = Depends(delete_account_use_case),
):
    await usecase.execute(current_user.id, account_id)
    return None
