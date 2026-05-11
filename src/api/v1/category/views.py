from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from api.v1.auth.dependencies import get_current_user
from infrastructure.database.postgresql.models import User
from usecases.category.create_category.abstract import AbstractCreateCategoryUseCase

from .dependencies import create_category_use_case
from .schemas import CreateCategorySchema


router = APIRouter(prefix="/category")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CreateCategorySchema,
    usecase: AbstractCreateCategoryUseCase = Depends(create_category_use_case),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    try:
        category = await usecase.execute(current_user.id, payload)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return category
