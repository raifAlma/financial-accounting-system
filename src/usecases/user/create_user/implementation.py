from api.v1.user.schemas import CreateUserSchema

from .abstract import AbstractCreateUserUseCase


class PostgreSQLCreateUserUseCase(AbstractCreateUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CreateUserSchema):
        async with self._uow as uow_:

            user = await uow_.repository.create(schema)

        return user
