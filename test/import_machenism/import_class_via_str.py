import importlib
from test.t1 import T1


class TestClass:

    def test_fun(self):
        print("You call method 'test_fun'.")



class MainClass:

    @classmethod
    def run(cls):
        # Test for import python file
        module = __import__("test_class")
        test_class = getattr(module, "TestClass")
        tc = test_class()
        tc.test_fun()

        # Test for import other folder (package source code)
        __pyocean = __import__("just_test")
        print("package: ", __pyocean)


    @classmethod
    def run_new(cls):
        T1.fun()



if __name__ == '__main__':

    # MainClass.run()
    MainClass.run_new()
