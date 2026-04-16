from pydantic import BaseModel
from datetime import datetime


class PurchaseBase(BaseModel):
    agent_id: int


class PurchaseCreate(PurchaseBase):
    user_id: int | None = None  # user_id підставляється автоматично з JWT


class PurchaseRead(PurchaseBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class PurchaseData(BaseModel):
    id: int
    agent_id: int
    timestamp: datetime
    agent_name: str | None = None
    agent_role: str | None = None
