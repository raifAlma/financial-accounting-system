from abc import ABC, abstractmethod

from api.v1.transaction.schemas import CreateTransactionSchema


class AbstractCreateTransactionUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: CreateTransactionSchema): ...
