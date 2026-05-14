from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.v1.budget.schemas import CreateBudgetSchema, ResponseBudgetSchema, UpdateBudgetSchema
from infrastructure.database.postgresql.models import Budget, Category, Transaction, Account


class PostgreSQLBudgetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, schema: CreateBudgetSchema) -> Budget:
        stmt_cat = select(Category).where(
            Category.id == schema.category_id,
            Category.user_id == user_id
        )
        result_cat = await self.session.execute(stmt_cat)
        category = result_cat.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        stmt_budget = select(Budget).where(
            Budget.category_id == schema.category_id,
            Budget.month == schema.month,
            Budget.user_id == user_id
        )
        result_budget = await self.session.execute(stmt_budget)
        existing_budget = result_budget.scalar_one_or_none()
        if existing_budget:
            raise HTTPException(status_code=409, detail="Budget for this category and month already exists")

        budget = Budget(
            user_id=user_id,
            category_id=schema.category_id,
            month=schema.month,
            planned_amount=schema.planned_amount,
            currency=schema.currency,
        )
        self.session.add(budget)
        await self.session.flush()
        return budget

    async def get_list(self, user_id:int) -> list[Budget]:
        stmt = (select(Budget)
            .where(Budget.user_id == user_id)
            .options(selectinload(Budget.category))
            .order_by(Budget.month))
        result = await self.session.execute(stmt)
        budgets = result.scalars().all()
        return budgets

    async def get(self, user_id: int, budget_id:int) -> Budget:
        stmt = (select(Budget)
            .where(Budget.user_id == user_id, Budget.id == budget_id)
            .options(selectinload(Budget.category))
            .order_by(Budget.month))
        result = await self.session.execute(stmt)
        budget = result.scalar_one_or_none()
        if not budget:
            raise HTTPException(404, "Budget not found")
        return budget

    async def update(self, user_id: int, budget_id: int, schema: UpdateBudgetSchema) -> Budget:
        stmt = select(Budget).options(selectinload(Budget.category)).where(
            Budget.user_id == user_id,
            Budget.id == budget_id
        )
        result = await self.session.execute(stmt)
        budget = result.scalar_one_or_none()
        if not budget:
            raise HTTPException(404, "Budget not found")

        update_data = schema.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            if hasattr(budget, field):
                setattr(budget, field, value)

        await self.session.flush()
        return budget


    async def delete(self, user_id: int, budget_id: int) -> None:
        stmt = (select(Budget).
                where(Budget.user_id == user_id, Budget.id == budget_id))
        result = await self.session.execute(stmt)
        budget = result.scalar_one_or_none()
        if not budget:
            raise HTTPException(404, "Budget not found")
        await self.session.delete(budget)



    async def budget_status(self, user_id: int, month: str) -> list[dict]:
        # 1. Вычисляем первый и последний день месяца
        # month = "2025-05"
        year, month_num = map(int, month.split('-'))
        start_date = datetime(year, month_num, 1).date()
        # Последний день: первый день следующего месяца минус 1 день
        if month_num == 12:
            next_month = datetime(year + 1, 1, 1).date()
        else:
            next_month = datetime(year, month_num + 1, 1).date()
        end_date = next_month - timedelta(days=1)

        # 2. Получаем все бюджеты пользователя за месяц с названием категории и валютой
        # Используем join с Category, чтобы сразу получить category_name
        stmt_budgets = select(
            Budget.category_id,
            Category.name.label('category_name'),
            Budget.planned_amount,
            Budget.currency
        ).join(Category, Category.id == Budget.category_id).where(
            Budget.user_id == user_id,
            Budget.month == month
        )
        result_budgets = await self.session.execute(stmt_budgets)
        budgets = result_budgets.all()  # кортежи: (category_id, category_name, planned_amount, currency)

        # 3. Получаем сумму расходов по категориям за месяц (только для этого пользователя)
        # Важно: в Transaction нет user_id, поэтому присоединяем Account
        stmt_spent = select(
            Transaction.category_id,
            func.sum(-Transaction.amount).label('actual_spent')  # делаем положительным
        ).join(Account, Account.id == Transaction.account_id).where(
            Account.user_id == user_id,  # фильтр по пользователю через счёт
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
            Transaction.amount < 0  # только расходы
        ).group_by(Transaction.category_id)
        result_spent = await self.session.execute(stmt_spent)
        # Превращаем результат в словарь: {category_id: actual_spent}
        spent_dict = {row.category_id: row.actual_spent for row in result_spent}

        # 4. Объединяем данные
        result = []
        for cat_id, cat_name, planned, currency in budgets:
            actual = spent_dict.get(cat_id, 0.0)
            diff = planned - actual
            percent = (actual / planned * 100) if planned != 0 else 0.0
            result.append({
                "category_id": cat_id,
                "category_name": cat_name,
                "planned_amount": float(planned),
                "actual_spent": float(actual),
                "difference": float(diff),
                "percentage": percent,
                "currency": currency
            })
        return result

