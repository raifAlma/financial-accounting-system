from abc import ABC, abstractmethod


class AbstractGetCategoryUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int, category_id: int): ...
