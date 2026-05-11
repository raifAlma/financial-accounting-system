from api.v1.account.schemas import CreateAccountSchema

from .abstract import AbstractCreateAccountUseCase


class PostgreSQLCreateAccountUseCase(AbstractCreateAccountUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, schema: CreateAccountSchema):
        async with self._uow as uow_:

            account = await uow_.repository.create(user_id, schema)

        return account
