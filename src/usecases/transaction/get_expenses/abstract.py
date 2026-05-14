from abc import ABC, abstractmethod


class AbstractGetExpensesUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int, month: str): ...
