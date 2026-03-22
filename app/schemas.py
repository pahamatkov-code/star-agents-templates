from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

# === КОРИСТУВАЧІ ===
class UserBase(BaseModel):
    email: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # сучасна заміна orm_mode


# === АГЕНТИ ===
class AgentBase(BaseModel):
    name: str
    role: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    skills: Optional[str] = None
    status: bool = True


class AgentCreate(AgentBase):
    pass


class AgentData(AgentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    purchases_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class AgentPartialUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    skills: Optional[str] = None
    status: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)


# === ПОКУПКИ ===
class PurchaseBase(BaseModel):
    user_id: int
    agent_id: int


class PurchaseCreate(PurchaseBase):
    pass


class Purchase(PurchaseBase):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class PurchaseData(BaseModel):
    id: int
    agent_id: int
    timestamp: datetime
    agent_name: Optional[str] = None
    agent_role: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# === АВТОРИЗАЦІЯ ===
class Token(BaseModel):
    access_token: str
    token_type: str
