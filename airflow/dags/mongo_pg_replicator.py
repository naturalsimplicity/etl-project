import logging

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
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
def mongo_data_generator():
    @task(task_id="load_product_price_history")
    def load_product_price_history():
        mongo = _get_mongodb_database()
        pg = _get_postgres_database()
        collection = mongo["ProductPriceHistory"]
        with pg.cursor() as cur:
            cur.execute("truncate table products")
            cur.execute("truncate table product_price_history")
            for doc in collection.find({}):
                cur.execute(
                    """insert into products (product_id, current_price, currency, etl_valid_from)
                    values (%s, %s, %s, %s)""",
                    (doc["product_id"], doc["current_price"], doc["currency"], datetime.now())
                )
                for change in doc["price_changes"]:
                    cur.execute(
                        """insert into product_price_history (product_id, timestamp, price, etl_valid_from)
                        values (%s, %s, %s, %s)""",
                        (doc["product_id"], change["timestamp"], change["price"], datetime.now())
                    )
        pg.commit()

    load_product_price_history()

mongo_data_generator()
