from api.v1.budget.schemas import CreateBudgetSchema

from .abstract import AbstractCreateBudgetUseCase


class PostgreSQLCreateBudgetUseCase(AbstractCreateBudgetUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, schema: CreateBudgetSchema):
        async with self._uow as uow_:

            budget = await uow_.repository.create(user_id, schema)

        return budget
