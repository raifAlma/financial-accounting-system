from abc import ABC, abstractmethod


class AbstractGetUserUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id: int): ...
