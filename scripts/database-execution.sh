#!/usr/bin/env bash

if echo $1 | grep -q "show_databases";
then
  mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD < ./tests/testing-database/test_sql/$DATABASE_DRIVER/show_database.sql
elif echo $1 | grep -q "create_database";
then
  mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD < ./tests/testing-database/test_sql/$DATABASE_DRIVER/create_database.sql
elif echo $1 | grep -q "create_table";
then
  mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD < ./tests/testing-database/test_sql/$DATABASE_DRIVER/create_table.sql
elif echo $1 | grep -q "insert_test_data_rows";
then
  mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD < ./tests/testing-database/test_sql/$DATABASE_DRIVER/insert_test_data_rows.sql
else
  echo "error"
fi
