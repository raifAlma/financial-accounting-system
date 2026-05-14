from pydantic import BaseModel, ConfigDict

from infrastructure.database.postgresql.models.categories import TransactionType


class CreateCategorySchema(BaseModel):
    category_name: str
    type: TransactionType

class ResponseCategorySchema(BaseModel):
    id: int
    name: str
    type: TransactionType

    model_config = ConfigDict(from_attributes=True)
