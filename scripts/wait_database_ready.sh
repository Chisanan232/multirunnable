#!/usr/bin/env bash

for i in `seq 1 10`;
do
  nc -z $DB_HOST $DB_PORT && echo Success && exit 0
  echo -n .
  sleep 5
done
echo Failed waiting for MySQL && exit 1
