from api.v1.user.schemas import UpdateUserSchema, UserSchema

from .abstract import AbstractUpdateUserUseCase


class PostgreSQLUpdateUserUseCase(AbstractUpdateUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: UpdateUserSchema, user_id: int) -> UserSchema:
        async with self._uow as uow_:

            user = await uow_.repository.update(schema, user_id)

        return user
