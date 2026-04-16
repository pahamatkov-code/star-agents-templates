from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import SessionLocal
from app.models import User
from app.schemas.auth import LoginRequest, TokenPair, RefreshRequest
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings


router = APIRouter(prefix="/auth", tags=["Auth"])


# -----------------------------
# DB dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access = create_access_token(user.id, user.role)
    refresh = create_refresh_token(user.id, user.role)

    return TokenPair(
        access_token=access,
        refresh_token=refresh,
    )


# -----------------------------
# REFRESH TOKENS
# -----------------------------
@router.post("/refresh", response_model=TokenPair)
def refresh_tokens(body: RefreshRequest):
    try:
        payload = jwt.decode(
            body.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id = int(payload["sub"])
    role = payload["role"]

    new_access = create_access_token(user_id, role)
    new_refresh = create_refresh_token(user_id, role)

    return TokenPair(
        access_token=new_access,
        refresh_token=new_refresh,
    )
