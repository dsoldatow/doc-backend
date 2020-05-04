"""create chat table

Revision ID: ef7912cd4cc1
Revises: 3512ac0ea775
Create Date: 2020-05-05 03:04:38.078385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef7912cd4cc1'
down_revision = '3512ac0ea775'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE chats(
            id_chat serial PRIMARY KEY,
            from_user integer NOT NULL,
            to_user integer NOT NULL,
            "timestamp" timestamp not null default now()
            );
        create table messages(
            id_message serial PRIMARY KEY,
            id_chat integer,
            from_user integer NOT NULL,
            to_user integer NOT NULL,
             message text not null default '',
            "timestamp" timestamp not null default now())
        ;
    """)


def downgrade():
    op.execute(
        """
        DROP TABLE chats;
        """
    )
