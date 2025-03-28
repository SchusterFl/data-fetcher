"""added new table

Revision ID: 7aa284480b70
Revises: 
Create Date: 2025-03-13 08:34:28.999031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7aa284480b70'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datasources',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('frequency', sa.Interval(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_datasources_id'), 'datasources', ['id'], unique=False)
    op.create_index(op.f('ix_datasources_name'), 'datasources', ['name'], unique=False)
    op.create_table('handlers',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('script', sa.Text(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_handlers_id'), 'handlers', ['id'], unique=False)
    op.create_index(op.f('ix_handlers_name'), 'handlers', ['name'], unique=False)
    op.create_table('outputs',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('strategy', sa.String(), nullable=False),
    sa.Column('retention_days', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_outputs_id'), 'outputs', ['id'], unique=False)
    op.create_index(op.f('ix_outputs_name'), 'outputs', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_outputs_name'), table_name='outputs')
    op.drop_index(op.f('ix_outputs_id'), table_name='outputs')
    op.drop_table('outputs')
    op.drop_index(op.f('ix_handlers_name'), table_name='handlers')
    op.drop_index(op.f('ix_handlers_id'), table_name='handlers')
    op.drop_table('handlers')
    op.drop_index(op.f('ix_datasources_name'), table_name='datasources')
    op.drop_index(op.f('ix_datasources_id'), table_name='datasources')
    op.drop_table('datasources')
    # ### end Alembic commands ###
