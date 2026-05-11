from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from api.v1.auth.dependencies import get_current_user
from infrastructure.database.postgresql.models import User
from infrastructure.repositories.postgres.user.exception import (
    EmailAlreadyExists,
    PassportNumberAlreadyExists,
    PhoneAlreadyExists,
    UserIsExists,
)
from usecases.user.create_user.abstract import AbstractCreateUserUseCase
from usecases.user.delete_user.abstract import AbstractDeleteUserUseCase
from usecases.user.update_user.abstract import AbstractUpdateUserUseCase

from .dependencies import (
    create_user_use_case,
    delete_user_use_case,
    update_user_use_case,
)
from .schemas import CreateUserSchema, UpdateUserSchema, UserSchema


router = APIRouter(prefix="/user")


@router.post("", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: CreateUserSchema,
    usecase: AbstractCreateUserUseCase = Depends(create_user_use_case),
) -> JSONResponse:
    try:
        user = await usecase.execute(payload)
    except UserIsExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@router.put("/me")
async def update_user(
    payload: UpdateUserSchema,
    usecase: AbstractUpdateUserUseCase = Depends(update_user_use_case),
    current_user: User = Depends(get_current_user),
):
    try:
        updated_user = await usecase.execute(current_user.id, payload)
    except (
        EmailAlreadyExists,
        PhoneAlreadyExists,
        PassportNumberAlreadyExists,
        UserIsExists,
    ) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return updated_user


@router.delete("/me", status_code=204)
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    usecase: AbstractDeleteUserUseCase = Depends(delete_user_use_case),
):
    await usecase.execute(current_user.id)
    return None
