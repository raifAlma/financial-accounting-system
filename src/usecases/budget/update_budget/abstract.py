from abc import ABC, abstractmethod

from api.v1.budget.schemas import UpdateBudgetSchema
from infrastructure.database.postgresql.models import Budget


class AbstractUpdateBudgetUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id: int, budget_id:int, schema: UpdateBudgetSchema) -> Budget: ...
