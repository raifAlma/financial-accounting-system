from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.category.schemas import CreateCategorySchema
from infrastructure.database.postgresql.models import Category


class PostgreSQLCategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, schema: CreateCategorySchema):
        stmt = select(Category).where(
            Category.user_id == user_id, Category.name == schema.category_name
        )
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        if category:
            raise HTTPException(status_code=400, detail="Category already exists")
        category = Category(
            user_id=user_id,
            name=schema.category_name,
            type=schema.type,
        )
        self.session.add(category)
        await self.session.flush()
        return category
