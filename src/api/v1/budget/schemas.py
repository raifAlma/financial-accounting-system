from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from api.v1.category.schemas import ResponseCategorySchema

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"

class CreateBudgetSchema(BaseModel):
    category_id: int
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$", description="YYYY-MM")
    planned_amount: float = Field(..., gt=0)
    currency: Currency = Field(default="RUB", max_length=3)



class ResponseBudgetSchema(CreateBudgetSchema):
    id: int
    category: ResponseCategorySchema

    model_config = ConfigDict(from_attributes=True)

class UpdateBudgetSchema(BaseModel):
    planned_amount: Optional[float] = Field(..., gt=0)
    currency: Optional[Currency] = None

