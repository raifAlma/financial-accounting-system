from sqlalchemy.ext.asyncio import AsyncSession

from container import Container
from infrastructure.repositories.postgres.token.uow import PostgreSQLTokenUnitOfWork
from infrastructure.repositories.postgres.user.uow import PostgreSQLUserUnitOfWork


def build_user_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLUserUnitOfWork:
    return Container.user_uow_factory(session=session)


def build_token_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLTokenUnitOfWork:
    return Container.token_uow_factory(session=session)
