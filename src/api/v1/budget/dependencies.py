from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_budget_unit_of_work
from infrastructure.repositories.postgres.budget import PostgreSQLBudgetUnitOfWork
from usecases.budget.create_budget.implementation import PostgreSQLCreateBudgetUseCase
from usecases.budget.delete_budget.implementation import PostgreSQLDeleteBudgetUseCase
from usecases.budget.get_budget.implementation import PostgreSQLGetBudgetUseCase
from usecases.budget.get_budget_status.implementation import PostgreSQLGetBudgetStatusUseCase
from usecases.budget.get_list_budget.implementation import PostgreSQLGetListBudgetUseCase
from usecases.budget.update_budget.implementation import PostgreSQLUpdateBudgetUseCase

def get_budget_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLBudgetUnitOfWork:
    return build_budget_unit_of_work(session)

def create_budget_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_budget_unit_of_work(session)
    return PostgreSQLCreateBudgetUseCase(uow=uow)

def delete_budget_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_budget_unit_of_work(session)
    return PostgreSQLDeleteBudgetUseCase(uow=uow)

def get_list_budget_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_budget_unit_of_work(session)
    return PostgreSQLGetListBudgetUseCase(uow=uow)

def get_budget_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_budget_unit_of_work(session)
    return PostgreSQLGetBudgetUseCase(uow=uow)

def get_budget_status_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_budget_unit_of_work(session)
    return PostgreSQLGetBudgetStatusUseCase(uow=uow)

def update_budget_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_budget_unit_of_work(session)
    return PostgreSQLUpdateBudgetUseCase(uow=uow)

