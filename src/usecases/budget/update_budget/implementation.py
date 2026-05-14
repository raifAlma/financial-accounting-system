from api.v1.budget.schemas import UpdateBudgetSchema
from infrastructure.database.postgresql.models import Budget

from .abstract import AbstractUpdateBudgetUseCase


class PostgreSQLUpdateBudgetUseCase(AbstractUpdateBudgetUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, budget_id:int, schema: UpdateBudgetSchema) -> Budget:
        async with self._uow as uow_:

            budget = await uow_.repository.update(user_id, budget_id, schema)

        return budget
