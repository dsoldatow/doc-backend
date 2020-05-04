"""create auth table

Revision ID: 9ae577eb1489
Revises: 
Create Date: 2020-05-03 23:27:53.839213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ae577eb1489'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE auth(
            id_user serial PRIMARY KEY,
            login VARCHAR (100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            is_doctor bool not null,
            "timestamp" timestamp not null default now()
            );
    """)


def downgrade():
    op.execute(
        """
        DROP TABLE auth;
        """
    )