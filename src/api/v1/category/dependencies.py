from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_category_unit_of_work
from infrastructure.repositories.postgres.category import PostgreSQLCategoryUnitOfWork
from usecases.category.create_category.implementation import (
    PostgreSQLCreateCategoryUseCase,
)
from usecases.category.delete_category.implementation import (
    PostgreSQLDeleteCategoryUseCase
)
from usecases.category.get_all_category.implementation import (
    PostgreSQLGetListAccountUseCase
)
from usecases.category.get_category.implementation import (
    PostgreSQLGetCategoryUseCase
)

def get_category_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLCategoryUnitOfWork:
    return build_category_unit_of_work(session)


def create_category_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_category_unit_of_work(session)
    return PostgreSQLCreateCategoryUseCase(uow=uow)

def delete_category_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_category_unit_of_work(session)
    return PostgreSQLDeleteCategoryUseCase(uow=uow)

def get_list_category_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_category_unit_of_work(session)
    return PostgreSQLGetListAccountUseCase(uow=uow)

def get_category_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_category_unit_of_work(session)
    return PostgreSQLGetCategoryUseCase(uow=uow)
