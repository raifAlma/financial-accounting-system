from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.v1.transaction.schemas import CreateTransactionSchema, TransactionFilters
from infrastructure.database.postgresql.models import Account, Category, Transaction, Budget


class PostgreSQlTransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self, user_id: int, account_id: int, schema: CreateTransactionSchema
    ) -> tuple[Transaction, str | None]:
        # 1. Получаем счёт и проверяем принадлежность пользователю
        stmt = select(Account).where(
            Account.id == account_id, Account.user_id == user_id
        )
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # 2. Получаем категорию (дополнительно проверим, что она принадлежит пользователю)
        stmt_cat = select(Category).where(
            Category.id == schema.category_id,
            Category.user_id == user_id
        )
        result = await self.session.execute(stmt_cat)
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # 3. Проверка достаточности средств (только для расходов)
        new_balance = account.balance + schema.amount
        if schema.amount < 0 and new_balance < 0:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        account.balance = new_balance

        # 4. Проверка бюджета (только для расходов)
        warning = None
        if schema.amount < 0:
            month_str = schema.transaction_date.strftime("%Y-%m")
            # Получаем бюджет на категорию и месяц
            budget_stmt = select(Budget).where(
                Budget.category_id == schema.category_id,
                Budget.user_id == user_id,
                Budget.month == month_str
            )
            budget = await self.session.execute(budget_stmt)
            budget = budget.scalar_one_or_none()
            if budget:
                # Сумма расходов за месяц без учёта текущей транзакции
                first_day = schema.transaction_date.replace(day=1)
                spent_stmt = select(func.sum(Transaction.amount)).where(
                    Transaction.category_id == schema.category_id,
                    #Transaction.user_id == user_id,
                    Transaction.transaction_date >= first_day,
                    Transaction.transaction_date <= schema.transaction_date,
                    Transaction.amount < 0
                )
                spent = await self.session.execute(spent_stmt)
                spent = spent.scalar() or Decimal('0')
                if abs(spent + schema.amount) > budget.planned_amount:
                    warning = (
                        f"Budget exceeded for category '{category.name}' in {month_str}. "
                        f"Planned: {budget.planned_amount}, spent so far: {abs(spent)}, "
                        f"including this operation: {abs(schema.amount)}"
                    )
        # 5. Создаём транзакцию
        transaction = Transaction(
            account_id=account_id,
            amount=schema.amount,
            currency=account.currency,
            category_id=schema.category_id,
            transaction_date=schema.transaction_date,
            description=schema.description,
        )
        self.session.add(transaction)
        await self.session.flush()
        return transaction, warning

    async def get_list(
            self,
            user_id: int,
            account_id: int,
            filters: TransactionFilters
    ) -> list[Transaction]:
        # Базовый запрос с join для проверки прав доступа
        stmt = (
            select(Transaction)
            .join(Account, Transaction.account_id == Account.id)
            .where(
                Transaction.account_id == account_id,
                Account.user_id == user_id
            )
        )

        # Добавляем фильтры, если они заданы
        if filters.from_date is not None:
            stmt = stmt.where(Transaction.transaction_date >= filters.from_date)
        if filters.to_date is not None:
            stmt = stmt.where(Transaction.transaction_date <= filters.to_date)
        if filters.category_id is not None:
            stmt = stmt.where(Transaction.category_id == filters.category_id)

        # Сортировка и пагинация
        stmt = stmt.order_by(Transaction.transaction_date.desc())
        stmt = stmt.limit(filters.limit).offset(filters.offset)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get(self, user_id:int, transaction_id:int) -> Transaction:
        stmt = select(Transaction)\
        .join(Account, Transaction.account_id == Account.id)\
        .where(
            Transaction.id == transaction_id,
            Account.user_id == user_id
        )
        result = await self.session.execute(stmt)
        transaction = result.scalar_one_or_none()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction

    async def get_expenses(self, user_id: int, month: str) -> list[tuple[int, str, Decimal]]:
        # Преобразуем "2025-05" в первый день месяца и последний
        year, month_num = map(int, month.split('-'))
        start_date = datetime(year, month_num, 1).date()
        # Последний день: берём первый день следующего месяца и вычитаем 1 день
        if month_num == 12:
            next_month = datetime(year + 1, 1, 1).date()
        else:
            next_month = datetime(year, month_num + 1, 1).date()
        end_date = next_month - timedelta(days=1)

        stmt = (
            select(
                Category.id,
                Category.name,
                func.sum(Transaction.amount).label('total_spent')
            )
            .join(Transaction, Transaction.category_id == Category.id)
            .where(
                Category.user_id == user_id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date,
                Transaction.amount < 0
            )
            .group_by(Category.id, Category.name)
        )
        result = await self.session.execute(stmt)
        rows = result.all()
        return rows

