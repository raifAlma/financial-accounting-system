from .abstract import AbstractGetCategoryUseCase


class PostgreSQLGetCategoryUseCase(AbstractGetCategoryUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, category_id: int):

        async with self._uow as uow_:

            category = await uow_.repository.get(user_id, category_id)
        return category
