from abc import ABC, abstractmethod


class AbstractGetAccountUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int, account_id: int): ...
