import logging

from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

_POSTGRES_CONN = "postgres_conn"
_POSTGRES_DATABASE_NAME = "destination"

log = logging.getLogger("airflow.task")

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
def pg_datamart_loader():
    @task(task_id="load_user_activity")
    def load_user_activity():
        pg = _get_postgres_database()
        with pg.cursor() as cur:
            table_name = "user_activity"
            cur.execute(f"truncate table {table_name}")
            cur.execute(f"""
                insert into {table_name}
                with
                  reviews as
                    (select user_id,
                            count(*) as reviews_cnt
                     from moderation_queue
                     group by user_id
                    ),
                  events as
                    (select user_id,
                            count(distinct timestamp::date) as days_active,
                            count(distinct case when timestamp > current_date - 30 then timestamp::date end) as days_active_last_month,
                            sum(case when event_type = 'order_placed' then 1 else 0 end) as orders_cnt
                     from event_logs el
                     group by user_id
                    ),
                  search as 
                    (select user_id, category as preferred_category
                     from (select user_id, category, row_number() over (partition by user_id order by count(*) desc) as rn
                           from search_queries
                           group by user_id, category) t
                     where rn = 1
                    ),
                  sessions as
                    (select user_id,
                            count(*) as sessions_cnt,
                            avg(array_length(pages_visited), 1) as avg_pages_visited
                     from user_sessions
                     group by user_id
                    )
                select s.user_id,
                       s.sessions_cnt,
                       s.avg_pages_visited,
                       coalesce(u.days_active, 0) as days_active,
                       coalesce(u.days_active_last_month, 0) as days_active_last_month,
                       coalesce(u.orders_cnt, 0) as orders_cnt,
                       coalesce(r.reviews_cnt, 0) as reviews_cnt,
                       se.preferred_category,
                       current_timestamp as etl_valid_from
                from sessions s
                left join events e on s.user_id = e.user_id
                left join reviews r on s.user_id = r.user_id
                left join search se on s.user_id = se.user_id
            """)
            count = cur.rowcount
        pg.commit()
        log.info(F"Inserted {count} rows to table {table_name}")

    @task(task_id="load_support_efficiency")
    def load_support_efficiency():
        pg = _get_postgres_database()
        with pg.cursor() as cur:
            table_name = "support_efficiency"
            cur.execute(f"truncate table {table_name}")
            cur.execute(f"""
                insert into {table_name}
                with
                  messages as 
                    (select ticket_id,
                            min(timestamp) as first_message_dt,
                            max(timestamp) as last_message_dt,
                            count(case when sender = 'support' then 1 end) as support_messages,
                            count(case when sender = 'user' then 1 end) as user_messages
                     from support_ticket_messages
                     group by ticket_id
                    ),
                  responses as 
                    (select ticket_id,
                            extract(minute from avg(response_time)) as avg_response_time_min
                     from (select ticket_id,
                                  case
                                    when sender = 'user'
                                      then lead(timestamp) over (partition by ticket_id order by timestamp) - timestamp
                                  end as response_time
                           from (select stm.*,
                                        case
                                          when sender = lag(sender) over (partition by ticket_id order by timestamp)
                                            then 0
                                          else 1
                                        end as flag_change
                                 from support_ticket_messages stm
                                ) t
                           where flag_change = 1
                          ) t2
                     group by ticket_id
                    )
                select st.ticket_id,
                       st.user_id,
                       st.status,
                       st.issue_type,
                       m.first_message_dt,
                       m.last_message_dt,
                       m.support_messages,
                       m.user_messages,
                       r.avg_response_time_min,
                       current_timestamp as etl_valid_from
                from support_tickets st
                join messages m on st.ticket_id = m.ticket_id
                left join responses r on st.ticket_id = r.ticket_id
                """)
            count = cur.rowcount
        pg.commit()
        log.info(F"Inserted {count} rows to table {table_name}")

    [load_user_activity(), load_support_efficiency()]

pg_datamart_loader()
