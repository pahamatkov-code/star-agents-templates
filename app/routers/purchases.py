from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas, models
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/purchases", tags=["Purchases"])


# === Створення покупки ===
@router.post("/", response_model=schemas.Purchase)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(models.Agent.id == purchase.agent_id).first()
    user = db.query(models.User).filter(models.User.id == purchase.user_id).first()

    if not agent or not user:
        raise HTTPException(status_code=404, detail="User or Agent not found")

    return crud.create_purchase(db=db, purchase=purchase)


# === Перегляд усіх покупок (адмін) ===
@router.get("/", response_model=List[schemas.Purchase])
def read_purchases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    purchases = crud.get_purchases(db, skip=skip, limit=limit)
    return purchases


# === Перегляд покупок поточного користувача ===
@router.get("/me", response_model=List[schemas.PurchaseData])
def read_my_purchases(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    purchases = db.query(models.Purchase).filter(models.Purchase.user_id == current_user.id).all()

    result = []
    for p in purchases:
        result.append(
            schemas.PurchaseData(
                id=p.id,
                agent_id=p.agent_id,
                timestamp=p.timestamp,
                agent_name=p.agent.name if p.agent else None,
                agent_role=p.agent.role if p.agent else None,
            )
        )
    return result


# === Видалення покупки ===
@router.delete("/{purchase_id}", response_model=schemas.Purchase)
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")

    db.delete(purchase)
    db.commit()
    return purchase
