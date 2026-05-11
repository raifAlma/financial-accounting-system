from api.v1.category.schemas import CreateCategorySchema

from .abstract import AbstractCreateCategoryUseCase


class PostgreSQLCreateCategoryUseCase(AbstractCreateCategoryUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, schema: CreateCategorySchema):
        async with self._uow as uow_:

            category = await uow_.repository.create(user_id, schema)

        return category
