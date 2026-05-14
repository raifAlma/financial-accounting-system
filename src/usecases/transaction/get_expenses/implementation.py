from .abstract import AbstractGetExpensesUseCase


class PostgreSQLGetExpensesUseCase(AbstractGetExpensesUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, month: str):

        async with self._uow as uow_:

            expenses = await uow_.repository.get(user_id, month)
        return expenses
