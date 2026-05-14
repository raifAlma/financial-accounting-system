from .abstract import AbstractGetBudgetUseCase


class PostgreSQLGetBudgetUseCase(AbstractGetBudgetUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, budget_id: int):

        async with self._uow as uow_:

            budget = await uow_.repository.get(user_id, budget_id)
        return budget
