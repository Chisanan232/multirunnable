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


