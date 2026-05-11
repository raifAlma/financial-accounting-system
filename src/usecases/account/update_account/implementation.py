from api.v1.account.schemas import AccountResponseSchema, AccountUpdateSchema

from .abstract import AbstractUpdateAccountUseCase


class PostgreSQLUpdateAccountUseCase(AbstractUpdateAccountUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(
        self, payload: AccountUpdateSchema, account_id, user_id: int
    ) -> AccountResponseSchema:
        async with self._uow as uow_:

            account = await uow_.repository.update(payload, account_id, user_id)

        return account
