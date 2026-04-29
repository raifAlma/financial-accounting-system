from .abstract import AbstractGetUserUseCase


class PostgreSQLGetUserUseCase(AbstractGetUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int):

        async with self._uow as uow_:

            user = await uow_.repository.get_user(user_id)
        return user
