FROM alpine:3.21

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install required modules
RUN pip install alembic psycopg2

# set workdir
WORKDIR /eshop

# Copy project files
COPY ./eshop .
