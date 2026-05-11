from abc import ABC, abstractmethod


class AbstractDeleteAccountUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id: int, account_id): ...
