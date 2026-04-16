from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.core.deps import get_db
from app.models import User, Agent, Purchase, BalanceTransaction
from app.core.security import get_password_hash

router = APIRouter(prefix="/seed", tags=["Seed"])


@router.post("")
def seed(db: Session = Depends(get_db)):

    # -------------------------
    # 1. Create admin
    # -------------------------
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            balance=0
        )
        db.add(admin)

    # -------------------------
    # 2. Create users
    # -------------------------
    users_data = [
        ("user1@example.com", "user123"),
        ("user2@example.com", "user123"),
        ("user3@example.com", "user123"),
    ]

    users = []
    for email, pwd in users_data:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                hashed_password=get_password_hash(pwd),
                role="user",
                balance=0
            )
            db.add(user)
        users.append(user)

    # -------------------------
    # 3. Create agents
    # -------------------------
    agent_names = ["ChatGPT", "Claude", "Gemini"]

    agents = []
    for name in agent_names:
        agent = db.query(Agent).filter(Agent.name == name).first()
        if not agent:
            agent = Agent(
                name=name,
                description=f"AI agent {name}",
                price=round(random.uniform(5, 20), 2)
            )
            db.add(agent)
        agents.append(agent)

    db.commit()

    # -------------------------
    # 4. Add random balance top-ups
    # -------------------------
    for user in users:
        amount = random.randint(50, 200)
        user.balance += amount

        tx = BalanceTransaction(
            user_id=user.id,
            amount=amount,
            type="topup"
        )
        db.add(tx)

    db.commit()

    # -------------------------
    # 5. Create random purchases
    # -------------------------
    for _ in range(20):
        user = random.choice(users)
        agent = random.choice(agents)
        amount = agent.price

        # Only create purchase if user has enough balance
        if user.balance < amount:
            continue

        user.balance -= amount

        purchase = Purchase(
            user_id=user.id,
            agent_id=agent.id,
            amount=amount,
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 14))
        )

        db.add(purchase)

    db.commit()

    return {"status": "ok", "message": "Seed data created successfully"}
