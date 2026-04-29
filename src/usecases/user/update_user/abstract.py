from abc import ABC, abstractmethod

from api.v1.user.schemas import UpdateUserSchema, UserSchema


class AbstractUpdateUserUseCase(ABC):
    @abstractmethod
    async def execute(self, user: UpdateUserSchema, user_id: int) -> UserSchema: ...
