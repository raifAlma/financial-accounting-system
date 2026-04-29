from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_user_unit_of_work
from infrastructure.repositories.postgres.user import PostgreSQLUserUnitOfWork
from usecases.user.create_user.implementation import PostgreSQLCreateUserUseCase
from usecases.user.delete_user.implementation import PostgreSQLDeleteUserUseCase
from usecases.user.get_user.implementation import PostgreSQLGetUserUseCase
from usecases.user.update_user.implementation import PostgreSQLUpdateUserUseCase


def get_user_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLUserUnitOfWork:
    return build_user_unit_of_work(session)


def create_user_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_user_unit_of_work(session)
    return PostgreSQLCreateUserUseCase(uow=uow)


def delete_user_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_user_unit_of_work(session)
    return PostgreSQLDeleteUserUseCase(uow=uow)


def get_user_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_user_unit_of_work(session)
    return PostgreSQLGetUserUseCase(uow=uow)


def update_user_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_user_unit_of_work(session)
    return PostgreSQLUpdateUserUseCase(uow=uow)
