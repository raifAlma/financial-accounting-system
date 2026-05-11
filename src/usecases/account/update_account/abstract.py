from abc import ABC, abstractmethod

from api.v1.account.schemas import AccountResponseSchema, AccountUpdateSchema


class AbstractUpdateAccountUseCase(ABC):
    @abstractmethod
    async def execute(
        self, payload: AccountUpdateSchema, account_id, user_id: int
    ) -> AccountResponseSchema: ...
