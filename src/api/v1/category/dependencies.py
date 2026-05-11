from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_category_unit_of_work
from infrastructure.repositories.postgres.category import PostgreSQLCategoryUnitOfWork
from usecases.category.create_category.implementation import (
    PostgreSQLCreateCategoryUseCase,
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
