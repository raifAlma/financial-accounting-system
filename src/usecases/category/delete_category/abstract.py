from abc import ABC, abstractmethod


class AbstractDeleteCategoryUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id: int, category_id: int): ...