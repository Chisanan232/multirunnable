#!/usr/bin/env bash

if echo $1 | grep -q "show_databases";
then
  mysql -h ${{ env.DB_HOST }} -u ${{ env.DB_USER }} -p${{ env.DB_PASSWORD }} ${{ env.DB_DATABASE }} < ./tests/testing-database/test_sql/${{ env.DATABASE_DRIVER }}/show_database.sql
elif echo $1 | grep -q "create_database";
then
  mysql -h ${{ env.DB_HOST }} -u ${{ env.DB_USER }} -p${{ env.DB_PASSWORD }} ${{ env.DB_DATABASE }} < ./tests/testing-database/test_sql/${{ env.DATABASE_DRIVER }}/create_database.sql
elif echo $1 | grep -q "create_table";
then
  mysql -h ${{ env.DB_HOST }} -u ${{ env.DB_USER }} -p${{ env.DB_PASSWORD }} ${{ env.DB_DATABASE }} < ./tests/testing-database/test_sql/${{ env.DATABASE_DRIVER }}/create_table.sql
elif echo $1 | grep -q "insert_test_data_rows";
then
  mysql -h ${{ env.DB_HOST }} -u ${{ env.DB_USER }} -p${{ env.DB_PASSWORD }} ${{ env.DB_DATABASE }} < ./tests/testing-database/test_sql/${{ env.DATABASE_DRIVER }}/insert_test_data_rows.sql
else
  echo "error"
fi
