from infrastructure.database.postgresql.models import Transaction
from .abstract import AbstractGetListTransactionUseCase


class PostgreSQLGetListTransactionUseCase(AbstractGetListTransactionUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, account_id:int)->list[Transaction]:

        async with self._uow as uow_:

           transaction = await uow_.repository.get_list(user_id, account_id)
        return transaction
