from typing import cast
import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable.api import retry
import time


# @retry.function
@retry.function(timeout=3)
def target_fail_function_with_default(*args, **kwargs) -> None:
    print("This is ExampleParallelClient.target_fail_function_with_default.")
    print("This is target function target_fail_function_with_default args: ", args)
    print("This is target function target_fail_function_with_default kwargs: ", kwargs)
    print("target_fail_function_with_default will raise exception after 3 seconds ...")
    time.sleep(3)
    raise Exception("Test for error")



# @retry.function
@retry.function(timeout=3)
def target_fail_function(*args, **kwargs) -> None:
    print("This is ExampleParallelClient.target_function.")
    print("This is target function args: ", args)
    print("This is target function kwargs: ", kwargs)
    print("It will raise exception after 3 seconds ...")
    time.sleep(3)
    raise Exception("Test for error")


@target_fail_function.initialization
def initial(*args, **kwargs):
    print("This is testing initialization of target_fail_function")
    print(f"This is testing initialization args of target_fail_function: {args}")
    print(f"This is testing initialization kwargs of target_fail_function: {kwargs}")


@target_fail_function.done_handling
def done(result):
    print("This is testing done process of target_fail_function")
    print("Get something result of target_fail_function: ", result)


@target_fail_function.final_handling
def final():
    # print(f"This is final process and result: {result}")
    print(f"This is final process and result of target_fail_function")


@target_fail_function.error_handling
def error(*args):
    print("This is error process of target_fail_function")
    print("Get something error of target_fail_function: ", args)



class RetryTest:

    @retry.bounded_function(timeout=3)
    def bounded_func_with_default(self, *args, **kwargs):
        print(f"[INFO] This is bounded function args: {args}")
        self.another(param_1="index_1", param_2="index_2")
        raise Exception("Test for error")


    @retry.bounded_function(timeout=3)
    def bounded_func(self, *args, **kwargs):
        print(f"[INFO] This is bounded function args: {args}")
        self.another(param_1="index_1", param_2="index_2")
        raise Exception("Test for error")


    def another(self, *args, **kwargs):
        print("[DEBUG] This is another method.")
        print(f"[DEBUG] This is another arg: {args}")
        print(f"[DEBUG] This is another kwargs: {kwargs}")


    @bounded_func.initialization
    def _bounded_init(self, *args, **kwargs):
        print("This is initialization process of bounded_func")
        print("Get something error of bounded_func args: ", args)
        print("Get something error of bounded_func kwargs: ", kwargs)


    @bounded_func.done_handling
    def _bounded_done(self, result):
        print("This is done process of bounded_func")
        print("Get something error of bounded_func: ", result)


    @bounded_func.error_handling
    def _bounded_error(self, *args):
        print("This is error process of bounded_func")
        print("Get something error of bounded_func: ", args)


    @bounded_func.final_handling
    def _bounded_final(self):
        print("This is final process of bounded_func")
        # print("Get something error of bounded_func: ", args)


    # @retry.bounded_function(timeout=3)
    @retry.function(timeout=3)
    @classmethod
    def classmethod_func(cls, *args, **kwargs):
        print(f"[INFO] This is classmethod function args: {args}")
        raise Exception("Test for error of classmethod_func")


    @classmethod_func.error_handling
    @classmethod
    def _classmethod_error(cls, *args):
        print("This is error process of classmethod_func")
        print("Get something error of classmethod_func: ", args)


    @retry.bounded_function(timeout=3)
    @staticmethod
    def staticmethod_func(*args, **kwargs):
        print(f"[INFO] This is staticmethod function args: {args}")
        raise Exception("Test for error of staticmethod_func")


    @staticmethod_func.error_handling
    @staticmethod
    def _staticmethod_error(*args):
        print("This is error process of staticmethod_func")
        print("Get something error of staticmethod_func: ", args)



class PolyRetryTest:

    @retry.bounded_function(timeout=3)
    def bounded_func_with_default(self, *args, **kwargs):
        print(f"[INFO] This is bounded function args: {args}")
        self.another(param_1="index_1", param_2="index_2")
        raise Exception("Test for error")


    @retry.bounded_function(timeout=3)
    def bounded_func(self, *args, **kwargs):
        print(f"[INFO] This is bounded function args: {args}")
        self.another(param_1="index_1", param_2="index_2")
        raise Exception("Test for error")


    def another(self, *args, **kwargs):
        print("[DEBUG] This is another method.")
        print(f"[DEBUG] This is another arg: {args}")
        print(f"[DEBUG] This is another kwargs: {kwargs}")


    @bounded_func.initialization
    def _bounded_init(self, *args, **kwargs):
        print("This is initialization process of bounded_func")
        print("Get something error of bounded_func args: ", args)
        print("Get something error of bounded_func kwargs: ", kwargs)


    @bounded_func.done_handling
    def _bounded_done(self, result):
        print("This is done process of bounded_func")
        print("Get something error of bounded_func: ", result)


    @bounded_func.error_handling
    def _bounded_error(self, *args):
        print("This is error process of bounded_func")
        print("Get something error of bounded_func: ", args)


    @bounded_func.final_handling
    def _bounded_final(self):
        print("This is final process of bounded_func")
        # print("Get something error of bounded_func: ", args)



class ATest:

    _rt = RetryTest()
    _prt = PolyRetryTest()

    def __init__(self):
        self._init_rt = RetryTest()

    def inner_func(self):
        # self._rt.bounded_func()
        # self._init_rt.bounded_func()
        self._prt.bounded_func()



class ASubTest(ATest):

    def inner_func(self):
        # self._rt.bounded_func()
        # self._prt.bounded_func()
        RetryTest.staticmethod_func()



class SubTest(RetryTest):

    def inner_func(self):
        self.bounded_func()


if __name__ == '__main__':

    print("This is executor client: ")
    try:
        target_fail_function_with_default()
    except Exception as e:
        print(f"[INFO in main] Got an exception: {e}")
    target_fail_function()

    _rt = RetryTest()
    # _rt: RetryTest = RetryTest()
    # _rt = cast(_rt, RetryTest)    # Doesn't consider about this situation currently.
    try:
        _rt.bounded_func_with_default()
    except Exception as e:
        print(f"[INFO in main] Got an exception: {e}")
    _rt.bounded_func()

    at = ATest()
    at.inner_func()

    at = ASubTest()
    at.inner_func()

    at = SubTest()
    at.inner_func()

    RetryTest.staticmethod_func()

    RetryTest.classmethod_func()    # Still has issue

