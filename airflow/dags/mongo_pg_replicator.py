import logging

from airflow.decorators import dag, task
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

_MONGO_DB_CONN = "mongo_db_conn"
_MONGO_DB_DATABASE_NAME = "origin"
_POSTGRES_CONN = "postgres_conn"
_POSTGRES_DATABASE_NAME = "destination"

log = logging.getLogger("airflow.task")

def _get_mongodb_database(
    mongo_db_conn_id: str = _MONGO_DB_CONN,
    mongo_db_database_name: str = _MONGO_DB_DATABASE_NAME
):
    hook = MongoHook(mongo_conn_id=mongo_db_conn_id)
    client = hook.get_conn()
    return client[mongo_db_database_name]

def _get_postgres_database(
    postgres_conn_id: str = _POSTGRES_CONN,
    postgres_database_name: str = _POSTGRES_DATABASE_NAME,
):
    hook = PostgresHook(postgres_conn_id=postgres_conn_id, database=postgres_database_name)
    return hook.get_conn()

default_args = {
    'owner': 'matvey',
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    default_args=default_args,
    start_date=datetime(2025, 3, 14, 12),
    schedule_interval='*/5 * * * *',  # every 5 minutes
    catchup=False
)
def mongo_pg_replicator():
    @task(task_id="load_product_price_history")
    def load_product_price_history():
        mongo = _get_mongodb_database()
        pg = _get_postgres_database()
        collection = mongo["ProductPriceHistory"]
        product_counter = 0
        product_price_history_counter = 0
        with pg.cursor() as cur:
            cur.execute("truncate table product")
            cur.execute("truncate table product_price_history")
            for doc in collection.find({}):
                cur.execute(
                    """insert into product (product_id, current_price, currency, etl_valid_from)
                    values (%s, %s, %s, %s)""",
                    (doc["product_id"], doc["current_price"], doc["currency"], datetime.now())
                )
                product_counter += 1
                for change in doc["price_changes"]:
                    cur.execute(
                        """insert into product_price_history (product_id, timestamp, price, etl_valid_from)
                        values (%s, %s, %s, %s)""",
                        (doc["product_id"], change["timestamp"], change["price"], datetime.now())
                    )
                    product_price_history_counter += 1
        pg.commit()
        log.info(F"Inserted {product_counter} rows to table product")
        log.info(F"Inserted {product_price_history_counter} rows to table product_price_history")

    @task(task_id="load_event_logs")
    def load_event_logs():
        mongo = _get_mongodb_database()
        pg = _get_postgres_database()
        collection = mongo["EventLogs"]
        table_name = "event_logs"
        counter = 0
        with pg.cursor() as cur:
            cur.execute(f"truncate table {table_name}")
            for doc in collection.find({}):
                cur.execute(
                    f"""insert into {table_name} (event_id, timestamp, event_type, user_id, ip_address, status, etl_valid_from)
                    values (%s, %s, %s, %s, %s, %s, %s)""",
                    (doc["event_id"], doc["timestamp"], doc["event_type"], doc["details"]["user_id"],
                    doc["details"]["ip_address"], doc["details"]["status"], datetime.now())
                )
                counter += 1
        pg.commit()
        log.info(F"Inserted {counter} rows to table {table_name}")

    @task(task_id="load_moderation_queue")
    def load_moderation_queue():
        mongo = _get_mongodb_database()
        pg = _get_postgres_database()
        collection = mongo["ModerationQueue"]
        table_name = "moderation_queue"
        counter = 0
        with pg.cursor() as cur:
            cur.execute(f"truncate table {table_name}")
            for doc in collection.find({}):
                cur.execute(
                    f"""insert into {table_name} (review_id, user_id, product_id, review_text, rating,
                        moderation_status, flags, submitted_at, etl_valid_from)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (doc["review_id"], doc["user_id"], doc["product_id"], doc["review_text"], doc["rating"],
                    doc["moderation_status"], doc["flags"], doc["submitted_at"], datetime.now())
                )
                counter += 1
        pg.commit()
        log.info(F"Inserted {counter} rows to table {table_name}")

    @task(task_id="load_search_queries")
    def load_search_queries():
        mongo = _get_mongodb_database()
        pg = _get_postgres_database()
        collection = mongo["SearchQueries"]
        table_name = "search_queries"
        counter = 0
        with pg.cursor() as cur:
            cur.execute(f"truncate table {table_name}")
            for doc in collection.find({}):
                cur.execute(
                    f"""insert into {table_name} (query_id, user_id, query_text, timestamp, category,
                    price_range, results_count, etl_valid_from)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (doc["query_id"], doc["user_id"], doc["query_text"], doc["timestamp"], doc["category"],
                    doc["price_range"], doc["results_count"], datetime.now())
                )
                counter += 1
        pg.commit()
        log.info(F"Inserted {counter} rows to table {table_name}")

    @task(task_id="load_support_tickets")
    def load_support_tickets():
        mongo = _get_mongodb_database()
        pg = _get_postgres_database()
        collection = mongo["SupportTickets"]
        table_name = "support_tickets"
        messages_table_name = "support_ticket_messages"
        counter = 0
        message_counter = 0
        with pg.cursor() as cur:
            cur.execute(f"truncate table {table_name}")
            cur.execute(f"truncate table {messages_table_name}")
            for doc in collection.find({}):
                cur.execute(
                    f"""insert into {table_name} (ticket_id, user_id, status, issue_type, created_at,
                    updated_at, etl_valid_from)
                    values (%s, %s, %s, %s, %s, %s, %s)""",
                    (doc["ticket_id"], doc["user_id"], doc["status"], doc["issue_type"], doc["created_at"],
                    doc["updated_at"], datetime.now())
                )
                counter += 1
                for message in doc["messages"]:
                    cur.execute(
                        f"""insert into {messages_table_name} (ticket_id, sender, message, timestamp, etl_valid_from)
                        values (%s, %s, %s, %s, %s)""",
                        (doc["ticket_id"], message["sender"], message["message"], message["timestamp"], datetime.now())
                    )
                    message_counter += 1
        pg.commit()
        log.info(F"Inserted {counter} rows to table {table_name}")
        log.info(F"Inserted {message_counter} rows to table {messages_table_name}")

    @task(task_id="load_user_recommendations")
    def load_user_recommendations():
        mongo = _get_mongodb_database()
        pg = _get_postgres_database()
        collection = mongo["UserRecommendations"]
        table_name = "user_recommendations"
        counter = 0
        with pg.cursor() as cur:
            cur.execute(f"truncate table {table_name}")
            for doc in collection.find({}):
                cur.execute(
                    f"""insert into {table_name} (user_id, recommended_products, last_updated, etl_valid_from)
                    values (%s, %s, %s, %s)""",
                    (doc["user_id"], doc["recommended_products"], doc["last_updated"], datetime.now())
                )
                counter += 1
        pg.commit()
        log.info(F"Inserted {counter} rows to table {table_name}")

    @task(task_id="load_user_sessions")
    def load_user_sessions():
        mongo = _get_mongodb_database()
        pg = _get_postgres_database()
        collection = mongo["UserSessions"]
        table_name = "user_sessions"
        actions_table_name = "user_session_actions"
        counter = 0
        action_counter = 0
        with pg.cursor() as cur:
            cur.execute(f"truncate table {table_name}")
            for doc in collection.find({}):
                cur.execute(
                    f"""insert into {table_name} (session_id, user_id, start_time, end_time, pages_visited,
                    device_type, device_user_agent, etl_valid_from)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (doc["session_id"], doc["user_id"], doc["start_time"], doc["end_time"],
                    doc["pages_visited"], doc["device"]["type"], doc["device"]["user_agent"], datetime.now())
                )
                counter += 1
                for action in doc["actions"]:
                    cur.execute(
                        f"""insert into {actions_table_name} (session_id, action_type, element, timestamp, etl_valid_from)
                        values (%s, %s, %s, %s, %s)""",
                        (doc["session_id"], action["action_type"], action["element"], action["timestamp"], datetime.now())
                    )
                    action_counter += 1
        pg.commit()
        log.info(F"Inserted {counter} rows to table {table_name}")
        log.info(F"Inserted {action_counter} rows to table {actions_table_name}")

    [load_product_price_history(), load_event_logs(), load_moderation_queue(), load_search_queries(),
     load_support_tickets(), load_user_recommendations(), load_user_sessions()]

mongo_pg_replicator()
