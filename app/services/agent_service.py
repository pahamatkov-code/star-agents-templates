from sqlalchemy.orm import Session
from app.models import Agent
from app.schemas.agent import AgentCreate, AgentUpdate


class AgentService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Agent).all()

    @staticmethod
    def get_by_id(db: Session, agent_id: int):
        return db.query(Agent).filter(Agent.id == agent_id).first()

    @staticmethod
    def create(db: Session, data: AgentCreate):
        agent = Agent(**data.dict())
        db.add(agent)
        db.commit()
        db.refresh(agent)
        return agent

    @staticmethod
    def update(db: Session, agent_id: int, data: AgentUpdate):
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(agent, key, value)

        db.commit()
        db.refresh(agent)
        return agent

    @staticmethod
    def delete(db: Session, agent_id: int):
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return False

        db.delete(agent)
        db.commit()
        return True
