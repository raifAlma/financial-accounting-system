from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.transaction.schemas import CreateTransactionSchema
from infrastructure.database.postgresql.models import Account, Category, Transaction


class PostgreSQlTransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, user_id: int, account_id: int, schema: CreateTransactionSchema
    ):
        stmt = select(Account).where(
            Account.id == account_id, Account.user_id == user_id
        )
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        smt = select(Category).where(Category.id == schema.category_id)
        result = await self.session.execute(smt)
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        transaction = Transaction(
            account_id=account_id,
            amount=schema.amount,
            currency=account.currency,
            category_id=schema.category_id,
            transaction_date=schema.transaction_date,
            description=schema.description,
        )

        account.balance += schema.amount
        self.session.add(transaction)
        await self.session.flush()
        return transaction
