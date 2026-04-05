from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from infrastructure.database.postgresql.session_manager import DatabaseSessionManager


class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)