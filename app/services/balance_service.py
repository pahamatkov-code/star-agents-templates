from sqlalchemy.orm import Session
from app.models import User, BalanceTransaction


class BalanceService:

    @staticmethod
    def topup(db: Session, user_id: int, amount: float):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        user.balance += amount

        tx = BalanceTransaction(
            user_id=user.id,
            amount=amount,
            type="topup"
        )

        db.add(tx)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_balance(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        return user.balance
