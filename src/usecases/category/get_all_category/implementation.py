from infrastructure.database.postgresql.models import Category
from .abstract import AbstractGetListCategoryUseCase


class PostgreSQLGetListAccountUseCase(AbstractGetListCategoryUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int)->list[Category]:

        async with self._uow as uow_:

            category = await uow_.repository.get_list(user_id)
        return category
