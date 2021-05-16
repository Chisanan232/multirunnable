from .t2 import T2
import importlib


class T1:

    @classmethod
    def fun(cls):
        # old
        # t2 = T2()
        # t2.fun()

        # test
        # t2_module = __import__("test.t2")
        # print("t2_module: ", t2_module)
        # t2_class = getattr(t2_module, "t2")
        # t2_instacne = t2_class.T2()
        # t2_instacne.fun()
        # print("t2_class: ", t2_class)

        # test for import .t2 via string-caller
        # __package = importlib.import_module(name=".t2", package="test")
        # print("__package: ", __package)
        # t2_class = getattr(__package, "T2")
        # t2_instacne = t2_class()
        # t2_instacne.fun()
        # print("t2_class: ", t2_class)


        # test for import .t2 via string-caller
        # __package = importlib.import_module(name=".t2", package="test")
        __package = importlib.import_module(name="test.t2", package="just_test")
        print("__package: ", __package)
        t2_class = getattr(__package, "T2")
        t2_instacne = t2_class()
        t2_instacne.fun()
        print("t2_class: ", t2_class)


# if __name__ == '__main__':
#
#     T1.fun()
