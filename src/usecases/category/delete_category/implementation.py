from .abstract import AbstractDeleteCategoryUseCase


class PostgreSQLDeleteCategoryUseCase(AbstractDeleteCategoryUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, category_id: int) -> None:

        async with self._uow as uow_:

            await uow_.repository.delete(user_id, category_id)
