from abc import ABC, abstractmethod

from api.v1.budget.schemas import CreateBudgetSchema


class AbstractCreateBudgetUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int, schema: CreateBudgetSchema): ...