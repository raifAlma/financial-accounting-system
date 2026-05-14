from abc import ABC, abstractmethod


class AbstractGetListTransactionUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int, account_id:int): ...