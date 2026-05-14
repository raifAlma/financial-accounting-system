from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from infrastructure.database.postgresql.models import User
from usecases.budget.create_budget.abstract import AbstractCreateBudgetUseCase
from usecases.budget.delete_budget.abstract import AbstractDeleteBudgetUseCase
from usecases.budget.get_budget.abstract import AbstractGetBudgetUseCase
from usecases.budget.get_budget_status.abstract import AbstractGetBudgetStatusUseCase
from usecases.budget.get_list_budget.abstract import AbstractGetListBudgetUseCase
from usecases.budget.update_budget.abstract import AbstractUpdateBudgetUseCase
from .schemas import CreateBudgetSchema, ResponseBudgetSchema, UpdateBudgetSchema

from .dependencies import (
    create_budget_use_case,
    delete_budget_use_case,
    get_list_budget_use_case,
    get_budget_use_case, update_budget_use_case, get_budget_status_use_case
)
from ..auth.dependencies import get_current_user

router = APIRouter(prefix='/budget')


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_budget(
    payload: CreateBudgetSchema,
    current_user: User = Depends(get_current_user),
    usecase: AbstractCreateBudgetUseCase = Depends(create_budget_use_case),
)->JSONResponse:
    budget = await usecase.execute(current_user.id, payload)
    return budget

@router.get('/{budget_id}',response_model=ResponseBudgetSchema)
async def get_budget(
        budget_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetBudgetUseCase = Depends(get_budget_use_case)
):
    budget = await usecase.execute(current_user.id, budget_id)
    return budget

@router.get("", response_model=list[ResponseBudgetSchema])
async def get_budget_list(
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetListBudgetUseCase = Depends(get_list_budget_use_case)
):
    budgets = await usecase.execute(current_user.id)
    return budgets

@router.get("")
async def get_budget_status(
        current_user: User = Depends(get_current_user),
        month: str = Query(..., description="YYYY-MM"),
        usecase: AbstractGetBudgetStatusUseCase = Depends(get_budget_status_use_case)
):
    budgets = await usecase.execute(current_user.id, month)
    return budgets

@router.put("/{budget_id}",response_model=ResponseBudgetSchema)
async def update_budget(
        payload: UpdateBudgetSchema,
        budget_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractUpdateBudgetUseCase = Depends(update_budget_use_case)
):
    budget = await usecase.execute(current_user.id, budget_id, payload)
    return budget

@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
        budget_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractDeleteBudgetUseCase = Depends(delete_budget_use_case)
):
    await usecase.execute(current_user.id, budget_id)
    return None