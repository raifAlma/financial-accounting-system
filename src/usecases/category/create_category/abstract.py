from abc import ABC, abstractmethod

from api.v1.category.schemas import CreateCategorySchema


class AbstractCreateCategoryUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: CreateCategorySchema): ...
