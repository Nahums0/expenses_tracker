"""Add default categories

Revision ID: 732873934cce
Revises: 802d5f1a1709
Create Date: 2023-10-21 15:36:10.598930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.database.models import Category, db


# revision identifiers, used by Alembic.
revision: str = '732873934cce'
down_revision: Union[str, None] = '802d5f1a1709'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

default_categories = [
    Category(id=0, categoryName="General", owner=None),
    Category(id=1, categoryName="Bills", owner=None),
    Category(id=2, categoryName="Rent", owner=None),
    Category(id=3, categoryName="Transportation", owner=None),
    Category(id=4, categoryName="Groceries", owner=None),
    Category(id=5, categoryName="Leisure", owner=None),
    Category(id=6, categoryName="Health", owner=None),
    Category(id=7, categoryName="Debt Repayment", owner=None),
    Category(id=8, categoryName="Education", owner=None),
    Category(id=9, categoryName="Personal Care", owner=None),
    Category(id=10, categoryName="Home Maintenance", owner=None),
    Category(id=11, categoryName="Shopping", owner=None),
    Category(id=12, categoryName="Gas", owner=None),
    Category(id=13, categoryName="Entertainment & Media", owner=None),
]


def upgrade() -> None:
    session = db.session

    session.add_all(default_categories)
    session.commit()

def downgrade() -> None:
    session = db.session

    categories_to_delete = (
        session.query(Category)
        .filter(Category.id.in_([c["id"] for c in default_categories]))
        .all()
    )

    for category in categories_to_delete:
        session.delete(category)
    session.commit()
