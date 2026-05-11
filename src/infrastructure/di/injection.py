from sqlalchemy.ext.asyncio import AsyncSession

from container import Container
from infrastructure.repositories.postgres.account.uow import PostgreSQLAccountUnitOfWork
from infrastructure.repositories.postgres.category.uow import (
    PostgreSQLCategoryUnitOfWork,
)
from infrastructure.repositories.postgres.token.uow import PostgreSQLTokenUnitOfWork
from infrastructure.repositories.postgres.transaction.uow import (
    PostgreSQLTransactionUnitOfWork,
)
from infrastructure.repositories.postgres.user.uow import PostgreSQLUserUnitOfWork


def build_user_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLUserUnitOfWork:
    return Container.user_uow_factory(session=session)


def build_token_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLTokenUnitOfWork:
    return Container.token_uow_factory(session=session)


def build_account_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLAccountUnitOfWork:
    return Container.account_uow_factory(session=session)


def build_transaction_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLTransactionUnitOfWork:
    return Container.transaction_uow_factory(session=session)


def build_category_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLCategoryUnitOfWork:
    return Container.category_uow_factory(session=session)
