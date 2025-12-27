"""update permission_role role_user role permission table

Revision ID: 36dcb9686a38
Revises: d488d94e7659
Create Date: 2025-12-27 14:25:17.312439
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36dcb9686a38'
down_revision: Union[str, Sequence[str], None] = 'd488d94e7659'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # permissions
    op.alter_column(
        'permissions',
        'description',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    # role_permissions
    op.add_column(
        'role_permissions',
        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()')
        )
    )
    op.add_column(
        'role_permissions',
        sa.Column(
            'updated_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()')
        )
    )

    # roles
    op.alter_column(
        'roles',
        'description',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    # user_roles
    op.add_column(
        'user_roles',
        sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()')
        )
    )
    op.add_column(
        'user_roles',
        sa.Column(
            'updated_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('NOW()')
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user_roles', 'updated_at')
    op.drop_column('user_roles', 'created_at')

    op.alter_column(
        'roles',
        'description',
        existing_type=sa.VARCHAR(),
        nullable=False
    )

    op.drop_column('role_permissions', 'updated_at')
    op.drop_column('role_permissions', 'created_at')

    op.alter_column(
        'permissions',
        'description',
        existing_type=sa.VARCHAR(),
        nullable=False
    )
