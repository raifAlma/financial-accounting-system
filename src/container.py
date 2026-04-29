from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from infrastructure.database.postgresql.session_manager import DatabaseSessionManager
from infrastructure.repositories.postgres.token import PostgreSQLTokenUnitOfWork
from infrastructure.repositories.postgres.user.uow import PostgreSQLUserUnitOfWork


class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    user_uow_factory = Factory(PostgreSQLUserUnitOfWork)
    token_uow_factory = Factory(PostgreSQLTokenUnitOfWork)
