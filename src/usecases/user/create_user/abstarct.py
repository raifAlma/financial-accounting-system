from abc import ABC, abstractmethod

from api.v1.user.schemas import CreateUserSchema


class AbstractCreateUserUseCase(ABC):
    @abstractmethod
    async def execute(self, user: CreateUserSchema): ...
