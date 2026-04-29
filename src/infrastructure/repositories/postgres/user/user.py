from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user.crypto import context
from api.v1.user.schemas import (
    CreateUserSchema,
    UpdateUserSchema,
    UserLoginSchema,
    UserSchema,
)
from infrastructure.database.postgresql.models import User

from .exception import (
    EmailAlreadyExists,
    PassportNumberAlreadyExists,
    PhoneAlreadyExists,
    UserIsExists,
    UserNotFound,
)


class PostgreSQLUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: CreateUserSchema):
        smt = select(User).where(User.email == payload.email)
        result = await self.session.execute(smt)
        existing_email = result.scalar_one_or_none()
        if existing_email:
            raise UserIsExists()
        user = User(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
            phone=payload.phone_number,
            passport=payload.passport_number,
        )

        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user(self, user_id: int) -> User:
        user = await self.session.get(User, user_id)
        if user is not None:
            user = UserSchema(id=user.id, full_name=user.full_name, email=user.email)
            return user
        raise HTTPException(status_code=404, detail="User not found")

    async def delete(self, user_id: int) -> None:
        user = await self.session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            await self.session.delete(user)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Cannot delete user")

    async def update(self, user_id: int, payload: UpdateUserSchema) -> UserSchema:
        user = await self.session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = payload.model_dump(exclude_unset=True)

        if "full_name" in update_data:
            new_name = update_data["full_name"]
            if new_name is None:
                raise HTTPException(status_code=400, detail="Full name cannot be null")
            # если full_name должен быть уникальным, добавь проверку

        if "email" in update_data:
            new_email = update_data["email"]
            if new_email is None:
                raise HTTPException(status_code=400, detail="Email cannot be null")
            stmt = select(User).where(User.email == new_email, User.id != user.id)
            result = await self.session.execute(stmt)
            existing_email = result.scalar_one_or_none()
            if existing_email:
                raise EmailAlreadyExists()

        if "phone" in update_data:  # поле в модели называется phone
            new_phone = update_data["phone"]
            if new_phone is None:
                raise HTTPException(status_code=400, detail="Phone cannot be null")
            stmt = select(User).where(User.phone == new_phone, User.id != user.id)
            result = await self.session.execute(stmt)
            existing_phone = result.scalar_one_or_none()
            if existing_phone:
                raise PhoneAlreadyExists()

        if "passport" in update_data:  # поле в модели называется passport
            new_passport = update_data["passport"]
            if new_passport is None:
                raise HTTPException(status_code=400, detail="Passport cannot be null")
            stmt = select(User).where(User.passport == new_passport, User.id != user.id)
            result = await self.session.execute(stmt)
            existing_passport = result.scalar_one_or_none()
            if existing_passport:
                raise PassportNumberAlreadyExists()

        # Обновляем поля
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        # Сохраняем изменения
        await self.session.flush()
        await self.session.refresh(user)

        return UserSchema(id=user.id, full_name=user.full_name, email=user.email)

    async def authorize(self, schema: UserLoginSchema) -> UserSchema | None:
        query = select(User).where(and_(User.full_name == schema.full_name))
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFound()

        verify = context.verify(schema.password, user.password)
        print(f"Username: {schema.full_name}")
        print(f"Password from request: {schema.password}")
        print(f"Password hash from DB: {user.password}")
        print(f"Verify result: {verify}")

        if not verify:
            raise HTTPException(status_code=400, detail="Incorrect password")

        return UserSchema(id=user.id, full_name=user.full_name, email=user.email)

    # async def get_by_id(self, user_id: int) -> User | None:
    #   return await self.session.get(User, user_id)
