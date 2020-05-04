"""create news

Revision ID: 3512ac0ea775
Revises: a626e94e1499
Create Date: 2020-05-04 23:21:48.005056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3512ac0ea775'
down_revision = 'a626e94e1499'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE news(
            id_news serial PRIMARY KEY,
            id_user integer not null, 
            description text not null default '',
            img text not null default '',
            link text not null default '',
            "timestamp" timestamp not null default now()
            );
    """)


def downgrade():
    op.execute(
        """
        DROP TABLE news;
        """
    )