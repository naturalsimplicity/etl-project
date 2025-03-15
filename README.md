# etl-project
HSE ETL processes project

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
    Username: <username from .env>
    Password: <password from .env>
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
    Login: <username from .env>
    Password: <password from .env>
    Port: 5433