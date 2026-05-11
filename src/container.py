from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from infrastructure.database.postgresql.session_manager import DatabaseSessionManager
from infrastructure.repositories.postgres.account.uow import PostgreSQLAccountUnitOfWork
from infrastructure.repositories.postgres.category import PostgreSQLCategoryUnitOfWork
from infrastructure.repositories.postgres.token import PostgreSQLTokenUnitOfWork
from infrastructure.repositories.postgres.transaction.uow import (
    PostgreSQLTransactionUnitOfWork,
)
from infrastructure.repositories.postgres.user.uow import PostgreSQLUserUnitOfWork


class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    user_uow_factory = Factory(PostgreSQLUserUnitOfWork)
    token_uow_factory = Factory(PostgreSQLTokenUnitOfWork)
    account_uow_factory = Factory(PostgreSQLAccountUnitOfWork)
    transaction_uow_factory = Factory(PostgreSQLTransactionUnitOfWork)
    category_uow_factory = Factory(PostgreSQLCategoryUnitOfWork)
