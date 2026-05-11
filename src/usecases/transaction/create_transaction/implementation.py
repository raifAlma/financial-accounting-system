from api.v1.transaction.schemas import CreateTransactionSchema

from .abstract import AbstractCreateTransactionUseCase


class PostgreSQLCreateTransactionUseCase(AbstractCreateTransactionUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, schema: CreateTransactionSchema):
        async with self._uow as uow_:

            transaction = await uow_.repository.create(
                user_id, schema.account_id, schema
            )

        return transaction
