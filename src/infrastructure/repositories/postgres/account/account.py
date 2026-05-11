from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.account.schemas import AccountUpdateSchema, CreateAccountSchema
from infrastructure.database.postgresql.models import Account


class PostgreSQLAccountRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, shema: CreateAccountSchema) -> Account:
        account = Account(
            user_id=user_id,
            name=shema.name,
            currency=shema.currency.value,
            balance=shema.balance,
            type=shema.type.value,
        )
        self.session.add(account)
        await self.session.flush()
        return account

    async def update(
        self, user_id: int, account_id, payload: AccountUpdateSchema
    ) -> Account:
        stmt = select(Account).where(
            Account.id == account_id, Account.user_id == user_id
        )
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(account, field):
                setattr(account, field, value)

        await self.session.flush()
        await self.session.refresh(account)
        return account

    async def delete(self, user_id: int, account_id: int) -> None:
        stmt = select(Account).where(
            Account.id == account_id, Account.user_id == user_id
        )
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if not account:
            raise HTTPException(404, "Account not found")
        await self.session.delete(account)
        await self.session.flush()
