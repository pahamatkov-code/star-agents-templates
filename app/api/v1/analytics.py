from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime

from app.core.deps import get_db, require_role
from app.models import Purchase, Agent, User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/purchases", dependencies=[Depends(require_role("admin"))])
def purchase_analytics(
    db: Session = Depends(get_db),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    user_id: int | None = Query(None),
    agent_id: int | None = Query(None),
):
    filters = []

    if date_from:
        filters.append(Purchase.created_at >= date_from)
    if date_to:
        filters.append(Purchase.created_at <= date_to)
    if user_id:
        filters.append(Purchase.user_id == user_id)
    if agent_id:
        filters.append(Purchase.agent_id == agent_id)

    # Загальна статистика
    total_purchases = db.query(func.count(Purchase.id)).filter(*filters).scalar()
    total_revenue = db.query(func.sum(Purchase.price)).filter(*filters).scalar() or 0
    unique_users = db.query(func.count(func.distinct(Purchase.user_id))).filter(*filters).scalar()

    # Найпопулярніший агент
    top_agent = (
        db.query(
            Agent.id,
            Agent.name,
            func.count(Purchase.id).label("cnt")
        )
        .join(Purchase, Purchase.agent_id == Agent.id)
        .filter(*filters)
        .group_by(Agent.id)
        .order_by(func.count(Purchase.id).desc())
        .first()
    )

    # Покупки по днях
    purchases_by_day = (
        db.query(
            func.date(Purchase.created_at).label("date"),
            func.count(Purchase.id).label("count"),
            func.sum(Purchase.price).label("revenue")
        )
        .filter(*filters)
        .group_by(func.date(Purchase.created_at))
        .order_by(func.date(Purchase.created_at))
        .all()
    )

    # ТОП-5 агентів
    top_agents = (
        db.query(
            Agent.id,
            Agent.name,
            func.count(Purchase.id).label("count"),
            func.sum(Purchase.price).label("revenue")
        )
        .join(Purchase, Purchase.agent_id == Agent.id)
        .filter(*filters)
        .group_by(Agent.id)
        .order_by(func.count(Purchase.id).desc())
        .limit(5)
        .all()
    )

    # ТОП-5 користувачів
    top_users = (
        db.query(
            User.id,
            User.email,
            func.sum(Purchase.price).label("spent")
        )
        .join(Purchase, Purchase.user_id == User.id)
        .filter(*filters)
        .group_by(User.id)
        .order_by(func.sum(Purchase.price).desc())
        .limit(5)
        .all()
    )

    return {
        "filters": {
            "date_from": date_from,
            "date_to": date_to,
            "user_id": user_id,
            "agent_id": agent_id,
        },
        "summary": {
            "total_purchases": total_purchases,
            "total_revenue": total_revenue,
            "unique_users": unique_users,
            "top_agent": {
                "id": top_agent.id if top_agent else None,
                "name": top_agent.name if top_agent else None,
                "count": top_agent.cnt if top_agent else None,
            },
        },
        "purchases_by_day": [
            {"date": str(row.date), "count": row.count, "revenue": row.revenue}
            for row in purchases_by_day
        ],
        "top_agents": [
            {"id": row.id, "name": row.name, "count": row.count, "revenue": row.revenue}
            for row in top_agents
        ],
        "top_users": [
            {"id": row.id, "email": row.email, "spent": row.spent}
            for row in top_users
        ],
    }