from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from app.core.config import settings


# -----------------------------
# Password hashing
# -----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Хешує пароль за допомогою bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевіряє відповідність пароля та хешу."""
    return pwd_context.verify(plain_password, hashed_password)


# -----------------------------
# JWT Token creation
# -----------------------------
def _create_token(data: dict, expires_delta: timedelta) -> str:
    """Створює JWT токен з часом життя."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_access_token(user_id: int, role: str) -> str:
    """Створює короткоживучий access token."""
    return _create_token(
        {"sub": str(user_id), "role": role, "type": "access"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(user_id: int, role: str) -> str:
    """Створює довгоживучий refresh token."""
    return _create_token(
        {"sub": str(user_id), "role": role, "type": "refresh"},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
