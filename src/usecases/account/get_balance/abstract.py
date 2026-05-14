from abc import ABC, abstractmethod

class AbstractGetBalanceUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id: int) -> dict[str, float]: ...