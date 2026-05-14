from abc import ABC, abstractmethod

from infrastructure.repositories.postgres.token.crypto import hash_token


class AbstractLogoutUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: hash_token): ...
