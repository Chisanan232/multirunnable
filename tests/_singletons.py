from multirunnable._singletons import (
    simple_singleton, singleton,     # Implement via function
    Singleton, NamedSingleton, ConnectionPoolSingleton,     # Implement via class
    SingletonMeta, NamedSingletonMeta, NamedSingletonABCMeta)     # Implement via meta class

from abc import abstractmethod
import pytest



@simple_singleton
class SimpleSingletonDecorateCls:

    __Index_Value = 0

    @property
    def index_val(self) -> int:
        return self.__Index_Value


    @index_val.setter
    def index_val(self, val: int) -> None:
        self.__Index_Value = val



@singleton
class SingletonDecoratorCls:

    __Index_Value = 0

    @property
    def index_val(self) -> int:
        return self.__Index_Value


    @index_val.setter
    def index_val(self, val: int) -> None:
        self.__Index_Value = val



class SingletonInheritCls(Singleton):

    __Index_Value = 0

    def __init__(self, **kwargs):
        self.test_parm = kwargs.get("test_parm", "")


    @property
    def index_val(self) -> int:
        return self.__Index_Value


    @index_val.setter
    def index_val(self, val: int) -> None:
        self.__Index_Value = val



class NamedSingletonInheritCls(NamedSingleton):

    __Index_Value = 0

    @property
    def index_val(self) -> int:
        return self.__Index_Value


    @index_val.setter
    def index_val(self, val: int) -> None:
        self.__Index_Value = val



class NamedSingletonInheritDiffCls(NamedSingleton):

    __Index_Value = 0

    @property
    def index_val(self) -> int:
        return self.__Index_Value


    @index_val.setter
    def index_val(self, val: int) -> None:
        self.__Index_Value = val



class ConnectionPoolSingletonInheritCls(ConnectionPoolSingleton):

    __Index_Value = 0

    def __init__(self, **kwargs):
        self.pool_name = kwargs.get("pool_name", "")


    @property
    def index_val(self) -> int:
        return self.__Index_Value


    @index_val.setter
    def index_val(self, val: int) -> None:
        self.__Index_Value = val



class ConnectionPoolSingletonInheritDiffCls(ConnectionPoolSingleton):

    __Index_Value = 0

    @property
    def index_val(self) -> int:
        return self.__Index_Value


    @index_val.setter
    def index_val(self, val: int) -> None:
        self.__Index_Value = val



class SingletonMetaCls(metaclass=SingletonMeta):

    __Index_Value = 0

    @property
    def index_val(self):
        return self.__Index_Value

    @index_val.setter
    def index_val(self, i):
        self.__Index_Value = i



class NamedSingletonMetaCls(metaclass=NamedSingletonMeta):

    __Index_Value = 0

    @property
    def index_val(self):
        return self.__Index_Value

    @index_val.setter
    def index_val(self, i):
        self.__Index_Value = i



class NamedSingletonMetaDiffCls(metaclass=NamedSingletonMeta):

    __Index_Value = 0

    @property
    def index_val(self):
        return self.__Index_Value

    @index_val.setter
    def index_val(self, i):
        self.__Index_Value = i



class AbstractNamedSingletonABCMetaCls(metaclass=NamedSingletonABCMeta):

    __Index_Value = 0

    @property
    @abstractmethod
    def index_val(self):
        pass



class NamedSingletonABCMetaCls(AbstractNamedSingletonABCMetaCls):

    __Index_Value = 0

    @property
    def index_val(self):
        return self.__Index_Value

    @index_val.setter
    def index_val(self, i):
        self.__Index_Value = i



class NamedSingletonABCMetaDiffCls(AbstractNamedSingletonABCMetaCls):

    __Index_Value = 0

    def __init__(self, **kwargs):
        self.test_param = kwargs.get("test_param", "no_value")


    @property
    def index_val(self):
        return self.__Index_Value

    @index_val.setter
    def index_val(self, i):
        self.__Index_Value = i



class TestSingletonsInOneThread:

    def test_simple_singleton_decorator(self):
        try:

            @simple_singleton
            def error_simple_singleton():
                pass

        except ValueError as e:
            assert "The target object be decorated should be a 'class' level type object" in str(
                e), f"It should raise an exception which content is this decorator should be used by 'class' object, doesn't by any others."
        else:
            assert False, f"It should raise an exception to tell developers this decorator should be used by 'class' object, doesn't by any others."

        TestSingletonsInOneThread._testing_singleton(
            instance=SimpleSingletonDecorateCls(),
            new_instance=SimpleSingletonDecorateCls()
        )


    def test_singleton_decorator(self):
        try:

            @singleton
            def error_singleton():
                pass

        except ValueError as e:
            assert "The target object be decorated should be a 'class' level type object" in str(
                e), f"It should raise an exception which content is this decorator should be used by 'class' object, doesn't by any others."
        else:
            assert False, f"It should raise an exception to tell developers this decorator should be used by 'class' object, doesn't by any others."

        TestSingletonsInOneThread._testing_singleton(
            instance=SingletonDecoratorCls(),
            new_instance=SingletonDecoratorCls()
        )


    def test_inherit_Singleton(self):
        _instn = SingletonInheritCls(test_parm="test_value")
        assert _instn.test_parm == "test_value", f"Its attribute *test_parm* should be same as we set."
        _new_instn = SingletonInheritCls()
        TestSingletonsInOneThread._testing_singleton(
            instance=_instn,
            new_instance=_new_instn
        )

        assert _instn.test_parm == _new_instn.test_parm == "", f"Its attribute *test_parm* should be empty because of 'SingletonInheritCls' with nothing parameters."


    def test_inherit_NamedSingleton(self):
        _instn = NamedSingletonInheritCls()
        _new_instn = NamedSingletonInheritCls()
        TestSingletonsInOneThread._testing_singleton(
            instance=_instn,
            new_instance=_new_instn
        )

        TestSingletonsInOneThread._testing_named_singleton(
            instance=_instn,
            diff_instance=NamedSingletonInheritDiffCls(),
            new_diff_instance=NamedSingletonInheritDiffCls()
        )


    def test_inherit_ConnectionPoolSingleton(self):
        _instn = ConnectionPoolSingletonInheritCls(pool_name="test_1")
        _new_instn = ConnectionPoolSingletonInheritCls(pool_name="test_1")
        TestSingletonsInOneThread._testing_singleton(
            instance=_instn,
            new_instance=_new_instn
        )

        assert _instn.pool_name == _new_instn.pool_name == "test_1", f"Its attribute *pool_name* should be same as we set."

        TestSingletonsInOneThread._testing_named_singleton(
            instance=_instn,
            diff_instance=ConnectionPoolSingletonInheritCls(pool_name="test_2"),
            new_diff_instance=ConnectionPoolSingletonInheritCls(pool_name="test_2")
        )


    def test_SingletonMeta(self):
        TestSingletonsInOneThread._testing_singleton(
            instance=SingletonMetaCls(),
            new_instance=SingletonMetaCls()
        )


    def test_NamedSingletonMeta(self):
        _instn = NamedSingletonMetaCls()
        _new_instn = NamedSingletonMetaCls()
        TestSingletonsInOneThread._testing_singleton(
            instance=_instn,
            new_instance=_new_instn
        )

        TestSingletonsInOneThread._testing_named_singleton(
            instance=_instn,
            diff_instance=NamedSingletonMetaDiffCls(),
            new_diff_instance=NamedSingletonMetaDiffCls()
        )


    def test_NamedSingletonABCMeta(self):
        _instn = NamedSingletonABCMetaCls()
        _new_instn = NamedSingletonABCMetaCls()
        TestSingletonsInOneThread._testing_singleton(
            instance=_instn,
            new_instance=_new_instn
        )

        _diff_instn = NamedSingletonABCMetaDiffCls(test_param="test_value")
        assert _diff_instn.test_param == "test_value", f"Its attribute *test_param* should be same as we set."

        _new_diff_instn = NamedSingletonABCMetaDiffCls()

        TestSingletonsInOneThread._testing_named_singleton(
            instance=_instn,
            diff_instance=_diff_instn,
            new_diff_instance=_new_diff_instn
        )

        assert _diff_instn.test_param == _new_diff_instn.test_param != "", f"Its attribute *test_parm* should not be empty because it will return instance directly if the key exists."

        _new_diff_instn.test_param = "reassign_value"
        assert _diff_instn.test_param == _new_diff_instn.test_param == "reassign_value", f"Its attribute *test_parm* should be modify because we modify it via instance, doesn't object."


    @staticmethod
    def _testing_singleton(instance, new_instance):
        for _ in range(2):
            instance.index_val += 1

        assert id(instance) == id(new_instance), f"The memory place which saving these instances should be the same."
        assert instance.index_val == new_instance.index_val == 2, f"The property 'index_val' value of both 2 instances should be '2' after it increases 2 with first instance."

        new_instance.index_val -= 1

        assert instance.index_val == new_instance.index_val == 1, f"The property 'index_val' value of both 2 instances should be '1' after it decreases 1 with new instance."


    @staticmethod
    def _testing_named_singleton(instance, diff_instance, new_diff_instance):
        diff_instance.index_val += 77

        assert diff_instance.index_val == new_diff_instance.index_val == 77, f"The property 'index_val' value of both 2 instances should be '77' after it increases 2 with first instance."
        assert diff_instance.index_val != instance.index_val, f"The property 'index_val' value of both 2 instances should be the same."
        assert id(diff_instance) == id(new_diff_instance), f"The memory place which saving these instances should be the same."
        assert id(diff_instance) != id(instance), f"The memory place which saving {instance.__class__.__name__} and {new_diff_instance.__class__.__name__} should be different."

