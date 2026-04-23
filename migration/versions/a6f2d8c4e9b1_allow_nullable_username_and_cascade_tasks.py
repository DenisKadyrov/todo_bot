"""allow nullable username and cascade tasks

Revision ID: a6f2d8c4e9b1
Revises: dd666e0995a9
Create Date: 2026-04-23 17:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a6f2d8c4e9b1"
down_revision: Union[str, None] = "dd666e0995a9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "username",
        existing_type=sa.String(),
        nullable=True,
    )
    op.drop_constraint("tasks_user_id_fkey", "tasks", type_="foreignkey")
    op.create_foreign_key(
        "tasks_user_id_fkey",
        "tasks",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("tasks_user_id_fkey", "tasks", type_="foreignkey")
    op.create_foreign_key(
        "tasks_user_id_fkey",
        "tasks",
        "users",
        ["user_id"],
        ["id"],
    )
    op.alter_column(
        "users",
        "username",
        existing_type=sa.String(),
        nullable=False,
    )
