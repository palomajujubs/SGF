"""novos campos model user

Revision ID: 8cf8b6881ba7
Revises: 4fa86267fbd2
Create Date: 2024-10-11 09:36:31.653946

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8cf8b6881ba7"
down_revision: Union[str, None] = "4fa86267fbd2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_hashed_password", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("username", sa.VARCHAR(), nullable=True),
        sa.Column("hashed_password", sa.VARCHAR(), nullable=True),
        sa.Column("email", sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=1)
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index(
        "ix_users_hashed_password", "users", ["hashed_password"], unique=False
    )
    op.create_index("ix_users_email", "users", ["email"], unique=1)
    # ### end Alembic commands ###
