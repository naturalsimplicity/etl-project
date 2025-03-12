#!/bin/bash
USER=mongo_user
PASSWORD=mongo_password
HOST=localhost
PORT=27017
DATABASE=origin

for FILE in ./data/*; do
	mongoimport \
  -c EventLogs \
  --type json \
  --file $FILE \
  --jsonArray \
  --authenticationDatabase=admin \
  "mongodb://${USER}:${PASSWORD}@${HOST}:${PORT}/${DATABASE}?authSource=admin"
  # "mongodb://mongo_user:mongo_password@localhost:27017/origin?authSource=admin"
done;
