from abc import ABC, abstractmethod

from api.v1.account.schemas import CreateAccountSchema


class AbstractCreateAccountUseCase(ABC):
    @abstractmethod
    async def execute(self, account: CreateAccountSchema): ...
