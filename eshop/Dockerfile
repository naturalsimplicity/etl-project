FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install required modules
RUN pip install alembic psycopg2-binary

# set workdir
WORKDIR /eshop

# Copy project files
COPY . .
