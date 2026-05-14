
from .abstract import AbstractGetAccountUseCase


class PostgreSQLGetAccountUseCase(AbstractGetAccountUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, account_id: int):

        async with self._uow as uow_:

            account = await uow_.repository.get(user_id, account_id)
        return account
