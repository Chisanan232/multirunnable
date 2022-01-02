from typing import Tuple, Dict
import os


# # # # Base APIs setting
Worker_Size: int = 7
Worker_Pool_Size: int = 7
Task_Size: int = 7

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

