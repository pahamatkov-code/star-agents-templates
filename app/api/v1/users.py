from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, require_role
from app.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# -----------------------------
# USER: отримати свій профіль
# -----------------------------
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


# -----------------------------
# ADMIN: отримати всіх користувачів
# -----------------------------
@router.get(
    "/",
    dependencies=[Depends(require_role("admin"))],
)
def get_all_users(
    db: Session = Depends(get_db),
):
    return db.query(User).all()
