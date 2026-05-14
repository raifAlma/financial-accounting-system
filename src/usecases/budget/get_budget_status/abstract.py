from abc import ABC, abstractmethod


class AbstractGetBudgetStatusUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int, month:str): ...
