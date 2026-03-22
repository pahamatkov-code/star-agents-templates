from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


# === КОРИСТУВАЧІ ===
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # Зв’язок із покупками
    purchases = relationship("Purchase", back_populates="user", cascade="all, delete-orphan")


# === АГЕНТИ ===
class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    role = Column(String(100), nullable=True, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    department = Column(String(100), nullable=True, index=True)
    skills = Column(Text, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Зв’язок із покупками
    purchases = relationship("Purchase", back_populates="agent", cascade="all, delete-orphan")


# === ПОКУПКИ ===
class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Зв’язки
    user = relationship("User", back_populates="purchases")
    agent = relationship("Agent", back_populates="purchases")
