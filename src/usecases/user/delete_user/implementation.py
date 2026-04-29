from .abstract import AbstractDeleteUserUseCase


class PostgreSQLDeleteUserUseCase(AbstractDeleteUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int) -> None:

        async with self._uow as uow_:

            await uow_.repository.delete(user_id)
