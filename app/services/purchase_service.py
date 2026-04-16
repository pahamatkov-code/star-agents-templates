from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import Purchase, User, Agent
from app.schemas.purchase import PurchaseCreate, PurchaseRead, PurchaseData


class PurchaseService:
    def __init__(self, db: Session):
        self.db = db

    # ============================
    # CREATE PURCHASE (atomic)
    # ============================
    def create_purchase(self, data: PurchaseCreate) -> Purchase:
        # Перевіряємо користувача
        user = self.db.query(User).filter(User.id == data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Перевіряємо агента
        agent = self.db.query(Agent).filter(Agent.id == data.agent_id).first()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )

        # Перевірка балансу
        if user.balance < agent.price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )

        # Atomic: списуємо баланс і створюємо покупку
        user.balance -= agent.price

        purchase = Purchase(
            user_id=user.id,
            agent_id=agent.id,
            price=agent.price,  # важливо: ціна на момент покупки
        )

        self.db.add(purchase)
        self.db.commit()
        self.db.refresh(purchase)

        return purchase

    # ============================
    # USER: get own purchases
    # ============================
    def get_purchases_by_user(self, user_id: int):
        purchases = (
            self.db.query(Purchase)
            .filter(Purchase.user_id == user_id)
            .order_by(Purchase.created_at.desc())
            .all()
        )

        result = []
        for p in purchases:
            result.append(
                PurchaseData(
                    id=p.id,
                    agent_id=p.agent_id,
                    price=p.price,
                    created_at=p.created_at,
                    agent_name=p.agent.name if p.agent else None,
                    agent_role=p.agent.role if p.agent else None,
                )
            )
        return result

    # ============================
    # ADMIN: get all purchases
    # ============================
    def get_all_purchases(self):
        return (
            self.db.query(Purchase)
            .order_by(Purchase.created_at.desc())
            .all()
        )

    # ============================
    # ADMIN: delete purchase
    # ============================
    def delete_purchase(self, purchase_id: int) -> bool:
        purchase = (
            self.db.query(Purchase)
            .filter(Purchase.id == purchase_id)
            .first()
        )

        if not purchase:
            return False

        self.db.delete(purchase)
        self.db.commit()
        return True
