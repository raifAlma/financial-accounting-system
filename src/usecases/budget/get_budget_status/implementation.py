from .abstract import AbstractGetBudgetStatusUseCase


class PostgreSQLGetBudgetStatusUseCase(AbstractGetBudgetStatusUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, month: str):

        async with self._uow as uow_:

            budget = await uow_.repository.budget_status(user_id, month)
        return budget
