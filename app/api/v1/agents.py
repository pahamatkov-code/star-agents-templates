from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_role
from app.schemas.agent import AgentCreate, AgentUpdate, AgentRead
from app.services.agent_service import AgentService

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


# -----------------------------
# ADMIN: отримати список агентів
# -----------------------------
@router.get(
    "/",
    response_model=List[AgentRead],
    dependencies=[Depends(require_role("admin"))],
)
def list_agents(
    db: Session = Depends(get_db),
):
    service = AgentService(db)
    return service.get_agents()


# -----------------------------
# ADMIN: отримати одного агента
# -----------------------------
@router.get(
    "/{agent_id}",
    response_model=AgentRead,
    dependencies=[Depends(require_role("admin"))],
)
def get_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    service = AgentService(db)
    agent = service.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    return agent


# -----------------------------
# ADMIN: створити агента
# -----------------------------
@router.post(
    "/",
    response_model=AgentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
def create_agent(
    data: AgentCreate,
    db: Session = Depends(get_db),
):
    service = AgentService(db)
    return service.create_agent(data)


# -----------------------------
# ADMIN: оновити агента
# -----------------------------
@router.put(
    "/{agent_id}",
    response_model=AgentRead,
    dependencies=[Depends(require_role("admin"))],
)
def update_agent(
    agent_id: int,
    data: AgentUpdate,
    db: Session = Depends(get_db),
):
    service = AgentService(db)
    agent = service.update_agent(agent_id, data)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    return agent


# -----------------------------
# ADMIN: видалити агента
# -----------------------------
@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin"))],
)
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    service = AgentService(db)
    deleted = service.delete_agent(agent_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    return None
