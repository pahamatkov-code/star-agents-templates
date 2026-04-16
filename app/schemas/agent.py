from pydantic import BaseModel
from datetime import datetime

class AgentBase(BaseModel):
    name: str
    role: str | None = None
    email: str | None = None
    department: str | None = None
    skills: str | None = None
    status: bool = True

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    email: str | None = None
    department: str | None = None
    skills: str | None = None
    status: bool | None = None

class AgentRead(AgentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
