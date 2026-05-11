from pydantic import BaseModel

from infrastructure.database.postgresql.models.categories import TransactionType


class CreateCategorySchema(BaseModel):
    category_name: str
    type: TransactionType
