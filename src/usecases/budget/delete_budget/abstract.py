from abc import ABC, abstractmethod


class AbstractDeleteBudgetUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id: int, budget_id: int): ...