from .abstract import AbstractGetTransactionUseCase


class PostgreSQLGetTransactionUseCase(AbstractGetTransactionUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, transaction_id: int):

        async with self._uow as uow_:

            transaction = await uow_.repository.get(user_id, transaction_id)
        return transaction
