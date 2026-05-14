from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user.schemas import UserSchema
from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_token_unit_of_work
from infrastructure.repositories.postgres.token import (
    PostgreSQLTokenRepository,
    PostgreSQLTokenUnitOfWork,
)
from usecases.token.create_token.implementation import PostgreSQLCreateTokenUseCase
from usecases.token.delete_refresh.implementation import PostgreSQLLogoutUseCase
from usecases.token.refresh_token.implementation import PostgreSQLRefreshTokenUseCase


def get_token_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLTokenUnitOfWork:
    return build_token_unit_of_work(session)


def create_token_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_token_unit_of_work(session)
    return PostgreSQLCreateTokenUseCase(uow=uow)


def refresh_token_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_token_unit_of_work(session)
    return PostgreSQLRefreshTokenUseCase(uow=uow)

def get_logout_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_token_unit_of_work(session)
    return PostgreSQLLogoutUseCase(uow=uow)


oauth2_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> UserSchema:
    token = credentials.credentials
    token_repo = PostgreSQLTokenRepository(session)
    user = await token_repo.get_user(token)
    if not user:
        raise HTTPException(401, "Invalid token")
    return user
