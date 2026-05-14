from abc import ABC, abstractmethod


class AbstractGetListBudgetUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int): ...
