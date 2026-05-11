from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateTransactionSchema(BaseModel):
    account_id: int
    category_id: int
    amount: Decimal
    description: Optional[str] = None
    transaction_date: date = Field(default_factory=date.today)

    @field_validator("amount")
    @classmethod
    def amount_not_zero(cls, value: Decimal) -> Decimal:
        if value == 0:
            raise ValueError("Amount cannot be zero")
        if abs(value) > 1_000_000:
            raise ValueError("Amount cannot exceed 1,000,000")
        return value


class TransactionResponseSchema(CreateTransactionSchema):
    id: int
    created_at: datetime
