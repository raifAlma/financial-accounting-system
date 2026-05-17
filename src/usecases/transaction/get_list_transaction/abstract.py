from abc import ABC, abstractmethod

from api.v1.transaction.schemas import TransactionFilters


class AbstractGetListTransactionUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int, account_id:int, filters: TransactionFilters): ...