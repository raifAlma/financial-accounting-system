from .abstract import AbstractGetBalanceUseCase

class PostgreSQLGetBalanceUseCase(AbstractGetBalanceUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int) -> dict[str, float]:
        async with self._uow as uow_:

            balances = await uow_.repository.get_balance(user_id)

        return {currency: float(total) for currency, total in balances}