from abc import ABC, abstractmethod


class AbstractGetTransactionUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int, transaction_id: int): ...
