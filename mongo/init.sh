#!/bin/bash
HOST=localhost
PORT=27017

for FILE in /sample_data/*; do
	mongoimport \
  -c "$(basename "${FILE%.*}")" \
  --type json \
  --file $FILE \
  --jsonArray \
  --authenticationDatabase=admin \
  "mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@${HOST}:${PORT}/${MONGO_INITDB_DATABASE}?authSource=admin"
  # "mongodb://mongo_user:mongo_password@localhost:27017/origin?authSource=admin"
done;
