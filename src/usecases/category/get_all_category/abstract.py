from abc import ABC, abstractmethod


class AbstractGetListCategoryUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id:int): ...
