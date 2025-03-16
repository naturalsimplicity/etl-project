from sqlalchemy import (
    Column, Integer, MetaData, String, Table, SmallInteger, table, Numeric
)

from sqlalchemy.dialects.postgresql import (
    UUID, TIMESTAMP, TEXT, ARRAY
)

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__%(all_column_names)s__'
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}

# Registry for all tables
metadata = MetaData(naming_convention=convention)

event_logs = Table(
    'event_logs',
    metadata,
    Column('event_id', UUID, primary_key=True),
    Column('timestamp', TIMESTAMP, nullable=False),
    Column('event_type', String(255), nullable=False),
    Column('user_id', Integer),
    Column('ip_address', String(255)),
    Column('status', String(255)),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

moderation_queue = Table(
    'moderation_queue',
    metadata,
    Column('review_id', UUID, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('product_id', Integer, nullable=False),
    Column('review_text', TEXT),
    Column('rating', SmallInteger),
    Column('moderation_status', String(255), nullable=False),
    Column('flags', ARRAY(String)),
    Column('submitted_at', TIMESTAMP, nullable=False),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

product = Table(
    'product',
    metadata,
    Column('product_id', Integer, primary_key=True),
    Column('current_price', Numeric(19, 2), nullable=False),
    Column('currency', String(5), nullable=False),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

product_price_history = Table(
    'product_price_history',
    metadata,
    Column('product_id', Integer, nullable=False),
    Column('timestamp', TIMESTAMP, nullable=False),
    Column('price', Numeric(19, 2), nullable=False),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

search_queries = Table(
    'search_queries',
    metadata,
    Column('query_id', UUID, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('query_text', TEXT),
    Column('timestamp', TIMESTAMP, nullable=False),
    Column('category', String(255)),
    Column('price_range', String(255)),
    Column('results_count', Integer),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

support_tickets = Table(
    'support_tickets',
    metadata,
    Column('ticket_id', UUID, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('status', String(255), nullable=False),
    Column('issue_type', String(255), nullable=False),
    Column('created_at', TIMESTAMP, nullable=False),
    Column('updated_at', TIMESTAMP, nullable=False),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

support_ticket_messages = Table(
    'support_ticket_messages',
    metadata,
    Column('ticket_id', UUID, nullable=False),
    Column('sender', String(255), nullable=False),
    Column('message', TEXT, nullable=False),
    Column('timestamp', TIMESTAMP, nullable=False),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

user_recommendations = Table(
    'user_recommendations',
    metadata,
    Column('user_id', Integer, nullable=False),
    Column('recommended_products', ARRAY(Integer)),
    Column('last_updated', TIMESTAMP, nullable=False),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

user_sessions = Table(
    'user_sessions',
    metadata,
    Column('session_id', UUID, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('start_time', TIMESTAMP, nullable=False),
    Column('end_time', TIMESTAMP, nullable=False),
    Column('pages_visited', ARRAY(String)),
    Column('device_type', String(255)),
    Column('device_user_agent', String),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

user_session_actions = Table(
    'user_session_actions',
    metadata,
    Column('session_id', UUID, nullable=False),
    Column('action_type', String(255), nullable=False),
    Column('element', String(255), nullable=True),
    Column('timestamp', TIMESTAMP, nullable=False),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

user_activity = Table(
    'user_activity',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('sessions_cnt', Integer, nullable=False),
    Column('avg_pages_visited', Numeric, nullable=False),
    Column('days_active', Integer, nullable=False),
    Column('days_active_last_month', Integer, nullable=False),
    Column('orders_cnt', Integer, nullable=False),
    Column('reviews_cnt', Integer, nullable=False),
    Column('preferred_category', String(255)),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)

support_efficiency = Table(
    'support_efficiency',
    metadata,
    Column('ticket_id', UUID, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('status', String(255), nullable=False),
    Column('issue_type', String(255), nullable=False),
    Column('first_message_dt', TIMESTAMP, nullable=False),
    Column('last_message_dt', TIMESTAMP, nullable=False),
    Column('support_messages', Integer, nullable=False),
    Column('user_messages', Integer, nullable=False),
    Column('avg_response_time_min', Numeric),
    Column('etl_valid_from', TIMESTAMP, nullable=False)
)
