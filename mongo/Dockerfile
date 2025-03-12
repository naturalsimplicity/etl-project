FROM mongo:latest
RUN apt-get update && \
    apt-get install -y mongodb-org-shell
COPY mongo/data mongo/init.sh
WORKDIR mongo
RUN ./init.sh