from .abstract import AbstractDeleteAccountUseCase


class PostgreSQLDeleteAccountUseCase(AbstractDeleteAccountUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, account_id: int) -> None:
        async with self._uow as uow:
            await uow.repository.delete(user_id, account_id)
