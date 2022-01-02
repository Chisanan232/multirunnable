from typing import Tuple, Dict


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

Database_Config = {
    "host": "127.0.0.1",
    "port": "3306",
    "user": "root",
    "password": "root",
    "database": "tw_stock"
}

Database_Pool_Config = {
    # "host": "127.0.0.1",
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "root",
    "database": "tw_stock",
    "pool_name": Test_Pool_Name,
    "pool_size": Test_Pool_Size
}

