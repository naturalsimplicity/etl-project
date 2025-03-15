# Use the official Airflow image as the base
FROM apache/airflow:2.10.5

# Set the AIRFLOW_HOME environment variable
ENV AIRFLOW_HOME=/usr/local/airflow

# install additional libraries
RUN pip install pymongo faker apache-airflow-providers-mongo

# Switch to the root user
USER root

# Create the AIRFLOW_HOME directory and change its ownership to the airflow user
RUN mkdir -p ${AIRFLOW_HOME} && chown -R airflow: ${AIRFLOW_HOME}

# Switch back to the airflow user
USER airflow

# Initialize the Airflow database
RUN airflow db init