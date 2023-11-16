"""Added a named field to the recurring transactions table

Revision ID: 78af826501d7
Revises: d71e8e1190d9
Create Date: 2023-11-07 17:44:02.718997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78af826501d7'
down_revision: Union[str, None] = 'd71e8e1190d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recurringTransactions', sa.Column('transactionName', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recurringTransactions', 'transactionName')
    # ### end Alembic commands ###