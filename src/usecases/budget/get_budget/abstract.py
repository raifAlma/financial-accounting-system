from abc import ABC, abstractmethod


class AbstractGetBudgetUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int, budget_id: int): ...
