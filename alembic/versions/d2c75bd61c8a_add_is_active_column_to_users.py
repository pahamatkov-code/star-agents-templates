"""add is_active column to users and create agents table

Revision ID: d2c75bd61c8a
Revises: 
Create Date: 2026-03-10 22:44:04.359641
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision: str = "d2c75bd61c8a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Таблиця users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # Таблиця agents
    op.create_table(
        "agents",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("role", sa.String(100), nullable=True),
        sa.Column("email", sa.String(255), nullable=True, unique=True),
        sa.Column("department", sa.String(100), nullable=True),
        sa.Column("skills", sa.Text(), nullable=True),
        sa.Column("status", sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_agents_name", "agents", ["name"])
    op.create_index("ix_agents_role", "agents", ["role"])
    op.create_index("ix_agents_department", "agents", ["department"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("agents")
    op.drop_table("users")
