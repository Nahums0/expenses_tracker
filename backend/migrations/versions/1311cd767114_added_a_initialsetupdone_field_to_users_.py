"""Added a initialSetupDone field to users table

Revision ID: 1311cd767114
Revises: 78af826501d7
Create Date: 2023-11-08 18:58:30.735778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1311cd767114'
down_revision: Union[str, None] = '78af826501d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('initialSetupDone', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'initialSetupDone')
    # ### end Alembic commands ###