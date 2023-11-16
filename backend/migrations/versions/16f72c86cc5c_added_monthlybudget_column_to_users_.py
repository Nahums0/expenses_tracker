"""Added monthlyBudget column to users table

Revision ID: 16f72c86cc5c
Revises: 34134247b29e
Create Date: 2023-11-14 18:59:15.914240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16f72c86cc5c'
down_revision: Union[str, None] = '34134247b29e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('monthlyBudget', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'monthlyBudget')
    # ### end Alembic commands ###
