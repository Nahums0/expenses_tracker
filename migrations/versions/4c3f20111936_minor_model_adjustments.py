"""Minor model adjustments

Revision ID: 4c3f20111936
Revises: 40093235e016
Create Date: 2023-10-22 15:25:42.714881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c3f20111936'
down_revision: Union[str, None] = '40093235e016'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userParsedCategory', sa.Column('userEmail', sa.String(length=255), nullable=True))
    op.drop_constraint('userParsedCategory_ownerEmail_fkey', 'userParsedCategory', type_='foreignkey')
    op.create_foreign_key(None, 'userParsedCategory', 'user', ['userEmail'], ['email'])
    op.drop_column('userParsedCategory', 'ownerEmail')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userParsedCategory', sa.Column('ownerEmail', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'userParsedCategory', type_='foreignkey')
    op.create_foreign_key('userParsedCategory_ownerEmail_fkey', 'userParsedCategory', 'user', ['ownerEmail'], ['email'])
    op.drop_column('userParsedCategory', 'userEmail')
    # ### end Alembic commands ###