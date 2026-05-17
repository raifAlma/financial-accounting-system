from fastapi import HTTPException

from api.v1.transaction.schemas import CreateTransactionSchema, TransactionResponseSchema
from infrastructure.database.postgresql.models.categories import TransactionType

from .abstract import AbstractCreateTransactionUseCase


class PostgreSQLCreateTransactionUseCase(AbstractCreateTransactionUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, schema: CreateTransactionSchema) -> tuple[
        TransactionResponseSchema, str | None]:
        async with self._uow as uow:
            # 1. Получить категорию (через репозиторий категорий, доступный в UoW)
            category = await uow.category_repository.get(user_id, schema.category_id)
            if not category or category.user_id != user_id:
                raise HTTPException(404, "Category not found")

            # 2. Определить знак суммы
            if category.type == TransactionType.EXPENSE:
                final_amount = -abs(schema.amount)
            else:
                final_amount = abs(schema.amount)

            # 3. Создать копию схемы с новым amount
            new_schema = CreateTransactionSchema(
                account_id=schema.account_id,
                category_id=schema.category_id,
                amount=final_amount,
                description=schema.description,
                transaction_date=schema.transaction_date
            )

            # 4. Вызвать репозиторий
            transaction, warning = await uow.repository.create(user_id, new_schema.account_id, new_schema)

        return TransactionResponseSchema.model_validate(transaction), warning