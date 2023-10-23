"""Changed date objects to datetime

Revision ID: b4047d47a4d2
Revises: 2fb0d95a09d6
Create Date: 2023-10-21 16:52:06.621832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4047d47a4d2'
down_revision: Union[str, None] = '2fb0d95a09d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recurringTransactions', 'startDate',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)
    op.alter_column('recurringTransactions', 'scannedAt',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)
    op.alter_column('transaction', 'paymentDate',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)
    op.alter_column('transaction', 'purchaseDate',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transaction', 'purchaseDate',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
    op.alter_column('transaction', 'paymentDate',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
    op.alter_column('recurringTransactions', 'scannedAt',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
    op.alter_column('recurringTransactions', 'startDate',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
    # ### end Alembic commands ###