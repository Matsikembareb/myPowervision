"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    # Check if vehicle table exists before creating
    import sqlalchemy as sa
    from alembic import op

    connection = op.get_bind()
    inspector = sa.inspect(connection)

    if 'vehicle' not in inspector.get_table_names():
        op.create_table('vehicle',
            # ... rest of your table creation code
        )

    # Continue with other migration operations...


def downgrade():
    ${downgrades if downgrades else "pass"}
