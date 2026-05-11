from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"


class AccountType(str, Enum):
    CASH = "cash"  # наличные
    CARD = "card"  # банковская карта (дебетовая)
    BANK_ACCOUNT = "bank"  # расчётный счёт
    CREDIT_CARD = "credit"  # кредитная карта
    INVESTMENT = "investment"  # инвестиционный


class CreateAccountSchema(BaseModel):
    name: str
    currency: Currency
    balance: Decimal
    type: AccountType


class AccountResponseSchema(BaseModel):
    id: int
    user_id: int
    name: str
    type: AccountType
    currency: Currency
    balance: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccountUpdateSchema(BaseModel):
    name: Optional[str]
    type: Optional[AccountType]
