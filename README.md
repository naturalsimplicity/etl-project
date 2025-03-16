# HSE ETL processes project

Проект реализует поставку данных и подготовку витрин для аналитики интернет-магазина.
Компоненты:
1. Оркестратор пайплайнов Apache Airflow
2. База данных MongoDB, в которой хранятся сырые данные. 
Наполнение синтетическими данными производится 
с помощью DAG'а `mongo_data_generator`
3. База данных PostgresSQL, в которую осуществляется 
поставка данных из базы данных сервиса (DAG `mongo_pg_replicator`) и
в которой производятся расчет аналитических витрин (DAG `pg_datamart_loader`)

## Деплой

### Docker

На виртуальной машине перед запуском docker-compose 
требуется создать .env файл аналогичный .env-dev, 
но с измененными секретами.

Для инициализации дагов и записи логов также требуется
убедиться, что у локальных директорий ./airflow/dags и ./airflow/logs 
имеются достаточные права и в случае необходимости выдать их:

    chmod -R 755 airflow

### Airflow

Перед первым запуском DAG'ов требуется настроить подключения к источникам
(Postgres, MongoDB) через Airflow UI со следующими параметрами

#### MongoDB

    Connection Id: mongo_db_conn
    Connection Type: MongoDB
    Host: mongo-origin
    Default DB: origin
    Username: <секрет из .env>
    Password: <секрет из .env>
    Port: 27017
    Extra: {
        "srv": false,
        "ssl": false,
        "allow_insecure": false,
        "authSource": "admin"
    }

#### Postgres

    Connection Id: postgres_conn
    Connection Type: Postgres
    Host: postgres-destination
    Database: destination
    Login: <секрет из .env>
    Password: <секрет из .env>
    Port: 5433

## Описание витрин

### user_activity - Активность пользователей

    user_id - идентификатор пользователя
    sessions_cnt - количество уникальных сессий
    avg_pages_visited - среднее количество просмотренных страниц за сессию
    days_active - количество дней, которые пользователь заходил в интернет-магазин
    days_active_last_month - количество дней, которые пользователь заходил в интернет-магазин за последний месяц
    orders_cnt - общее количество заказов
    reviews_cnt - количество оставленных отзывов на товары
    preferred_category - наиболее предпочитаемая категория товаров
    etl_valid_from - техническая дата актуальности записи

### support_efficiency - Эффективность поддержки

    ticket_id - идентификатор тикета (заявки в поддержку)
    user_id - идентификатор пользователя
    status - статус заявки
    issue_type - тип проблемы
    first_message_dt - дата и время первого сообщения в тикете
    last_message_dt - дата и время последнего сообщения в тикете
    support_messages - количество сообщений от сотрудника поддержки
    user_messages - количество сообщения от пользователя
    avg_response_time_min - средняя длительность ответа сотрудника поддержки в минутах
    etl_valid_from - техническая дата актуальности записи
