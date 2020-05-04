"""create users profile table

Revision ID: b646f98aa242
Revises: a9724f3e6a8c
Create Date: 2020-05-03 23:54:20.838111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b646f98aa242'
down_revision = 'a9724f3e6a8c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE user_profiles(
            id_user integer unique,
            name text not null default '',
            surname text not null default '',
            last_name text not null default '',
            city text not null default '',
            description text not null default ''
            );
    """)


def downgrade():
    op.execute(
        """
        DROP TABLE user_profiles;
        """
    )
