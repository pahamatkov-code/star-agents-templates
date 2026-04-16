from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, require_role
from app.schemas.purchase import PurchaseCreate, PurchaseRead
from app.services.purchase_service import PurchaseService
from app.models import User

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"],
)


# -----------------------------
# USER: створити покупку
# -----------------------------
@router.post(
    "/",
    response_model=PurchaseRead,
    status_code=status.HTTP_201_CREATED,
)
def create_purchase(
    data: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data.user_id = current_user.id
    return PurchaseService(db).create_purchase(data)


# -----------------------------
# USER: переглянути свої покупки
# -----------------------------
@router.get(
    "/my",
    response_model=list[PurchaseRead],
)
def get_my_purchases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PurchaseService(db).get_by_user(current_user.id)


# -----------------------------
# ADMIN: переглянути всі покупки
# -----------------------------
@router.get(
    "/",
    response_model=list[PurchaseRead],
    dependencies=[Depends(require_role("admin"))],
)
def get_all_purchases(
    db: Session = Depends(get_db),
):
    return PurchaseService(db).get_all()


# -----------------------------
# ADMIN: видалити покупку
# -----------------------------
@router.delete(
    "/{purchase_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin"))],
)
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
):
    deleted = PurchaseService(db).delete_purchase(purchase_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found",
        )
    return None
