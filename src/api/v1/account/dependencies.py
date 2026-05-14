from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_account_unit_of_work
from infrastructure.repositories.postgres.account import PostgreSQLAccountUnitOfWork
from usecases.account.create_account.implementation import (
    PostgreSQLCreateAccountUseCase,
)
from usecases.account.delete_account.implementation import (
    PostgreSQLDeleteAccountUseCase,
)
from usecases.account.get_account.implemenation import (
    PostgreSQLGetAccountUseCase,
)
from usecases.account.get_balance.implementation import PostgreSQLGetBalanceUseCase
from usecases.account.update_account.implementation import (
    PostgreSQLUpdateAccountUseCase,
)
from usecases.account.get_list_account.implementation import (
    PostgreSQLGetListAccountUseCase,
)


def get_account_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLAccountUnitOfWork:
    return build_account_unit_of_work(session)


def create_account_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_account_unit_of_work(session)
    return PostgreSQLCreateAccountUseCase(uow=uow)


def get_account_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_account_unit_of_work(session)
    return PostgreSQLGetAccountUseCase(uow=uow)

def get_list_account_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_account_unit_of_work(session)
    return PostgreSQLGetListAccountUseCase(uow=uow)

def get_balance_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_account_unit_of_work(session)
    return PostgreSQLGetBalanceUseCase(uow=uow)

def update_account_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_account_unit_of_work(session)
    return PostgreSQLUpdateAccountUseCase(uow=uow)


def delete_account_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_account_unit_of_work(session)
    return PostgreSQLDeleteAccountUseCase(uow=uow)
