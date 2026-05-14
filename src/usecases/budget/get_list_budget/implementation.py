from infrastructure.database.postgresql.models import Budget
from .abstract import AbstractGetListBudgetUseCase


class PostgreSQLGetListBudgetUseCase(AbstractGetListBudgetUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int)->list[Budget]:

        async with self._uow as uow_:

           budget = await uow_.repository.get_list(user_id)
        return budget
