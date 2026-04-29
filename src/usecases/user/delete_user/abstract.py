from abc import ABC, abstractmethod


class AbstractDeleteUserUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id: int): ...
