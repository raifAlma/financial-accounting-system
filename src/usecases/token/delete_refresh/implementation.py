from .abstract import AbstractLogoutUseCase

class PostgreSQLLogoutUseCase(AbstractLogoutUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, refresh_token: str) -> None:
        async with self._uow as uow:
            await uow.repository.delete_refresh_token(refresh_token)
