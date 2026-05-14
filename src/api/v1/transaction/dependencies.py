from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_transaction_unit_of_work
from infrastructure.repositories.postgres.transaction import (
    PostgreSQLTransactionUnitOfWork,
)
from usecases.transaction.create_transaction.implementation import (
    PostgreSQLCreateTransactionUseCase,
)
from usecases.transaction.get_expenses.implementation import PostgreSQLGetExpensesUseCase
from usecases.transaction.get_transaction.implementation import (
    PostgreSQLGetTransactionUseCase,
)
from usecases.transaction.get_list_transaction.implementation import (
    PostgreSQLGetListTransactionUseCase,
)


def get_transaction_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLTransactionUnitOfWork:
    return build_transaction_unit_of_work(session)


def create_transaction_use_case(session: AsyncSession = Depends(get_async_session)):
    uow = get_transaction_unit_of_work(session)
    return PostgreSQLCreateTransactionUseCase(uow=uow)

def get_list_transaction_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_transaction_unit_of_work(session)
    return PostgreSQLGetListTransactionUseCase(uow=uow)

def get_transaction_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_transaction_unit_of_work(session)
    return PostgreSQLGetTransactionUseCase(uow=uow)

def get_expenses_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_transaction_unit_of_work(session)
    return PostgreSQLGetExpensesUseCase(uow=uow)
