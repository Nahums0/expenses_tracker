"""Modified UserWarnings table

Revision ID: 1bbb11937a66
Revises: 8750d20a1635
Create Date: 2023-10-28 17:26:47.697694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bbb11937a66'
down_revision: Union[str, None] = '8750d20a1635'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userWarnings', sa.Column('failedLoginCount', sa.Integer(), nullable=False))
    op.drop_column('userWarnings', 'warningCount')
    op.drop_column('userWarnings', 'warningType')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userWarnings', sa.Column('warningType', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('userWarnings', sa.Column('warningCount', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('userWarnings', 'failedLoginCount')
    # ### end Alembic commands ###