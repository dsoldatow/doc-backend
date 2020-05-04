"""create profile table

Revision ID: a9724f3e6a8c
Revises: 9ae577eb1489
Create Date: 2020-05-03 23:28:12.415238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9724f3e6a8c'
down_revision = '9ae577eb1489'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE doctor_profiles(
            id_user integer unique,
            name text not null default '',
            surname text not null default '',
            last_name text not null default '',
            company text not null default '',
            city text not null default '',
            spec text not null default '',
            description text not null default '',
            img text not null default ''
            );
    """)


def downgrade():
    op.execute(
        """
        DROP TABLE doctor_profiles;
        """
    )
