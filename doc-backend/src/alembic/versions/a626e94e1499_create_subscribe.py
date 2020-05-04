"""create subscribe

Revision ID: a626e94e1499
Revises: b646f98aa242
Create Date: 2020-05-04 22:58:12.747814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a626e94e1499'
down_revision = 'b646f98aa242'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE subscribe(
            follower integer unique,
            main_person integer unique,
            "timestamp" timestamp not null default now()
            );
    """)


def downgrade():
    op.execute(
        """
        DROP TABLE subscribe;
        """
    )