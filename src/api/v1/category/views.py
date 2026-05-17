from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from api.v1.auth.dependencies import get_current_user
from infrastructure.database.postgresql.models import User
from usecases.category.create_category.abstract import AbstractCreateCategoryUseCase
from usecases.category.delete_category.abstract import AbstractDeleteCategoryUseCase
from usecases.category.get_all_category.abstract import AbstractGetListCategoryUseCase
from usecases.category.get_category.abstract import AbstractGetCategoryUseCase

from .dependencies import (
    create_category_use_case,
    get_category_use_case,
    delete_category_use_case,
    get_list_category_use_case
)
from .schemas import CreateCategorySchema, ResponseCategorySchema


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

@router.get("/{category_id}", response_model=ResponseCategorySchema)
async def get_category(
        category_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetCategoryUseCase = Depends(get_category_use_case)
):
    category = await usecase.execute(current_user.id, category_id)
    return category

@router.get('', response_model=list[ResponseCategorySchema])
async def get_list(
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetListCategoryUseCase = Depends(get_list_category_use_case)
):
    category = await usecase.execute(current_user.id)
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractDeleteCategoryUseCase = Depends(delete_category_use_case)
):
    await usecase.execute(current_user.id, category_id)
    return None