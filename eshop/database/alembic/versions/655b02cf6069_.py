"""Init migration

Revision ID: 655b02cf6069
Revises:
Create Date: 2025-03-15 19:53:08.155266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '655b02cf6069'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_logs',
    sa.Column('event_id', sa.UUID(), nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('event_type', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ip_address', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('event_id', name=op.f('pk__event_logs'))
    )
    op.create_table('moderation_queue',
    sa.Column('review_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('review_text', sa.TEXT(), nullable=True),
    sa.Column('rating', sa.SmallInteger(), nullable=True),
    sa.Column('moderation_status', sa.String(length=255), nullable=False),
    sa.Column('flags', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('submitted_at', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('review_id', name=op.f('pk__moderation_queue'))
    )
    op.create_table('product',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('current_price', sa.Numeric(precision=19, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=5), nullable=False),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('product_id', name=op.f('pk__product'))
    )
    op.create_table('product_price_history',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('price', sa.Numeric(precision=19, scale=2), nullable=False),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False)
    )
    op.create_table('search_queries',
    sa.Column('query_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('query_text', sa.TEXT(), nullable=True),
    sa.Column('timestamp', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('price_range', sa.String(length=255), nullable=True),
    sa.Column('results_count', sa.Integer(), nullable=True),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('query_id', name=op.f('pk__search_queries'))
    )
    op.create_table('support_ticket_messages',
    sa.Column('ticket_id', sa.UUID(), nullable=False),
    sa.Column('sender', sa.String(length=255), nullable=False),
    sa.Column('message', sa.TEXT(), nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False)
    )
    op.create_table('support_tickets',
    sa.Column('ticket_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.Column('issue_type', sa.String(length=255), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('ticket_id', name=op.f('pk__support_tickets'))
    )
    op.create_table('user_recommendations',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('recommended_products', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('last_updated', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False)
    )
    op.create_table('user_session_actions',
    sa.Column('session_id', sa.UUID(), nullable=False),
    sa.Column('action_type', sa.String(length=255), nullable=False),
    sa.Column('element', sa.String(length=255), nullable=True),
    sa.Column('timestamp', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False)
    )
    op.create_table('user_sessions',
    sa.Column('session_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('start_time', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('end_time', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('pages_visited', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('device_type', sa.String(length=255), nullable=True),
    sa.Column('device_user_agent', sa.String(), nullable=True),
    sa.Column('etl_valid_from', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('session_id', name=op.f('pk__user_sessions'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_sessions')
    op.drop_table('user_session_actions')
    op.drop_table('user_recommendations')
    op.drop_table('support_tickets')
    op.drop_table('support_ticket_messages')
    op.drop_table('search_queries')
    op.drop_table('product_price_history')
    op.drop_table('product')
    op.drop_table('moderation_queue')
    op.drop_table('event_logs')
    # ### end Alembic commands ###