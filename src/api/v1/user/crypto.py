from passlib.context import CryptContext


context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return context.hash(password)


from datetime import datetime, timedelta, timezone

from jose import jwt

from config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
