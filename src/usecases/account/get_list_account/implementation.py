from infrastructure.database.postgresql.models import Account
from .abstract import AbstractGetListAccountUseCase


class PostgreSQLGetListAccountUseCase(AbstractGetListAccountUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int)->list[Account]:

        async with self._uow as uow_:

            account = await uow_.repository.get_list(user_id)
        return account
