from multirunnable import RunningMode
from typing import Tuple, Dict
import os


Under_Test_RunningModes = [RunningMode.Parallel, RunningMode.Concurrent, RunningMode.GreenThread]

Under_Test_RunningModes_Without_Greenlet = [RunningMode.Parallel, RunningMode.Concurrent]

# # # # Base APIs setting
Worker_Size: int = 7
Worker_Pool_Size: int = 7
Task_Size: int = 3

Running_Diff_Time: int = 2

Test_Function_Sleep_Time = 3
Test_Function_Args: Tuple = (1, 2, "test_value")
Test_Function_Kwargs: Dict = {"param_1": 1, "param_2": 2, "test_param": "test_value"}
Test_Function_Multiple_Args = (Test_Function_Args, Test_Function_Args, Test_Function_Args)


# # # # Lock APIs setting
Semaphore_Value = 2


# # # # Persistence - Database setting
Test_Pool_Name = "testing_pool"
Test_Pool_Size = 2
Test_Pool_Size_ZERO = 0

database_host = (os.getenv("DB_HOST") or "127.0.0.1")
database_port = (os.getenv("DB_PORT") or 3306)
database_user = (os.getenv("DB_USER") or "root")
database_password = (os.getenv("DB_PASSWORD") or "password")
database_db = (os.getenv("DB_DATABASE") or "tw_stock")

Database_Config = {
    "host": database_host,
    "port": database_port,
    "user": database_user,
    "password": database_password,
    "database": database_db
}

Database_Pool_Config = {
    "host": database_host,
    "port": database_port,
    "user": database_user,
    "password": database_password,
    "database": database_db,
    "pool_name": Test_Pool_Name,
    "pool_size": Test_Pool_Size
}

Table_Columns = ('stock_date', 'trade_volume', 'turnover_price', 'opening_price', 'highest_price', 'lowest_price', 'closing_price', 'gross_spread', 'turnover_volume')

SELECT_TEST_DATA_SQL = "SELECT * FROM tw_stock.stock_data_2330 WHERE stock_date = '0100-01-01 00:00:00';"
INSERT_TEST_DATA_SQL = "INSERT INTO tw_stock.stock_data_2330 (stock_date, trade_volume, turnover_price, opening_price, highest_price, lowest_price, closing_price, gross_spread, turnover_volume) VALUES ('0100-01-01 00:00:00' , 51255446 ,11006827093 ,212.0000 ,216.5000 , 211.0000 ,215.5000 ,+4.50 , 14098);"
DELETE_TEST_DATA_SQL = "DELETE FROM tw_stock.stock_data_2330 WHERE stock_date = '0100-01-01 00:00:00';"

TEST_DATA_ROWS = [
    ('0100-01-01 00:00:00', 51255446, 11006827093, 212.0000, 216.5000, 211.0000, 215.5000, '+4.50', 14098),
    ('0100-01-02 00:00:00', 51255446, 11006827093, 212.0000, 216.5000, 211.0000, 215.5000, '+4.50', 14098),
    ('0100-01-03 00:00:00', 51255446, 11006827093, 212.0000, 216.5000, 211.0000, 215.5000, '+4.50', 14098)
]

SELECT_TEST_DATA_SQL_WITH_OPTION = "SELECT * FROM tw_stock.stock_data_2330 WHERE stock_date >= '0100-01-01 00:00:00' AND stock_date <= '0100-01-03 00:00:00';"
INSERT_TEST_DATA_SQL_WITH_OPTION = "INSERT INTO tw_stock.stock_data_2330 (stock_date, trade_volume, turnover_price, opening_price, highest_price, lowest_price, closing_price, gross_spread, turnover_volume) VALUES (%s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s);"
DELETE_TEST_DATA_SQL_WITH_OPTION = "DELETE FROM tw_stock.stock_data_2330 WHERE stock_date >= '0100-01-01 00:00:00' AND stock_date <= '0100-01-03 00:00:00';"
