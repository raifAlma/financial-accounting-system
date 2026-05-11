from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.repositories.postgres.token import PostgreSQLTokenRepository
from infrastructure.repositories.postgres.token.exception import InvalidRefreshToken
from infrastructure.repositories.postgres.user import PostgreSQLUserRepository
from infrastructure.repositories.postgres.user.exception import UserNotFound
from usecases.token.create_token.abstract import AbstractCreateTokenUseCase
from usecases.token.refresh_token.abstract import AbstractRefreshTokenUseCase

from .dependencies import create_token_use_case, refresh_token_use_case
from .schemas import RefreshTokenSchema, TokenSchema, UserLoginSchema


router = APIRouter(prefix="/auth")


# @router.post("/token", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
async def create_token(
    payload: UserLoginSchema,
    usecase: AbstractCreateTokenUseCase = Depends(create_token_use_case),
) -> JSONResponse:

    try:
        token = await usecase.execute(payload)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=token.model_dump(mode="json")
    )


@router.post(
    "/token/refresh", response_model=TokenSchema, status_code=status.HTTP_201_CREATED
)
async def refresh_token(
    payload: RefreshTokenSchema,
    usecase: AbstractRefreshTokenUseCase = Depends(refresh_token_use_case),
) -> JSONResponse:
    try:
        token = await usecase.execute(payload)
    except InvalidRefreshToken as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=token.model_dump(mode="json")
    )


# @router.post("/token", response_model=TokenSchema)
async def login(
    login_data: UserLoginSchema, session: AsyncSession = Depends(get_async_session)
):
    user_repo = PostgreSQLUserRepository(session)
    user = await user_repo.authorize(login_data)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    token_repo = PostgreSQLTokenRepository(session)
    token_data = await token_repo.create(user)
    await session.commit()  # вся логика в репозитории
    return token_data


@router.post("/token", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def create_token(
    payload: UserLoginSchema,
    usecase: AbstractCreateTokenUseCase = Depends(create_token_use_case),
):
    try:
        token = await usecase.execute(payload)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    # except HTTPException from authorize (неверный пароль) просто пробрасывается
    return token  # FastAPI сам сериализует
