from typing import Callable
import os
import logging

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.providers.mongo.hooks.mongo import MongoHook
from datetime import datetime, timedelta
from samples import generator

_MONGO_DB_CONN = os.getenv("MONGO_DB_CONN")
_MONGO_DB_DATABASE_NAME = os.getenv("MONGO_DB_DATABASE_NAME")

log = logging.getLogger("airflow.task")

def _get_mongodb_database(
    mongo_db_conn_id: str = _MONGO_DB_CONN,
    mongo_db_database_name: str = _MONGO_DB_DATABASE_NAME,
):
    hook = MongoHook(mongo_conn_id=mongo_db_conn_id)
    client = hook.get_conn()
    return client[mongo_db_database_name]

def _insert_docs(collection_name: str, gen_func: Callable, sample_size=10, insert_once=False):
    db = _get_mongodb_database()
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        log.info(f"Created collection {collection_name}")
    collection = db[collection_name]
    if insert_once and len(db.find({}, limit=1)) > 0:
        log.info(f"Collection {collection_name} already have documents, skipping")
        return
    collection.insert_many([gen_func(i+1) for i in range(sample_size)])
    log.info(f"Inserted {sample_size} docs into collection {collection_name}")

default_args = {
    'owner': 'matvey',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    default_args=default_args,
    start_date=datetime(2025, 3, 14, 12),
    schedule_interval='5 * * * *',  # every 5 minutes
    catchup=False
)
def mongo_data_generator():
    @task(task_id="gen_product_price_history")
    def gen_product_price_history():
        _insert_docs("ProductPriceHistory",
                     generator.gen_product_price_history,
                     sample_size=generator.MAX_PRODUCTS,
                     insert_once=True)

    @task(task_id="gen_event_logs")
    def gen_event_logs():
        _insert_docs("EventLogs", generator.gen_event_logs)

    @task(task_id="gen_moderation_queue")
    def gen_moderation_queue():
        _insert_docs("ModerationQueue", generator.gen_moderation_queue)

    @task(task_id="gen_search_queries")
    def gen_search_queries():
        _insert_docs("SearchQueries", generator.gen_search_queries)

    @task(task_id="gen_support_tickets")
    def gen_support_tickets():
        _insert_docs("SupportTickets", generator.gen_support_tickets)

    @task(task_id="gen_user_recommendations")
    def gen_user_recommendations():
        _insert_docs("UserRecommendations", generator.gen_user_recommendations)

    @task(task_id="gen_user_sessions")
    def gen_user_sessions():
        _insert_docs("UserSessions", generator.gen_user_sessions)

    chain(
        gen_product_price_history(),
        [gen_event_logs(), gen_moderation_queue(), gen_search_queries(), gen_support_tickets(),
         gen_user_recommendations(), gen_user_sessions()]
    )

mongo_data_generator()
