"""
A unittest for pyocean.task module
"""

from multirunnable.mode import RunningMode
from multirunnable.tasks import QueueTask
from multirunnable.parallel import ProcessQueueType
from multirunnable.concurrent import ThreadQueueType
from multirunnable.coroutine import GeventQueueType, AsynchronousQueueType

from abc import ABCMeta, abstractmethod
import random
import pytest


_Testing_Queue_Task_Name = "pytest_queue_task"
_Testing_Global_Queue_Task_Name = "testing_global"
_Testing_Queue_Task_Type = ProcessQueueType.Queue
_Testing_Queue_Task_Value = [random.randrange(1, 20) for _ in range(10)]


@pytest.fixture(scope="function")
def queue_task() -> QueueTask:
    return QueueTask()


class QueueTaskTestCases(metaclass=ABCMeta):

    @abstractmethod
    def test_name_operator(self, queue_task):
        pass


    @abstractmethod
    def test_queue_type_operator(self, queue_task):
        pass


    @abstractmethod
    def test_value_operator(self, queue_task):
        pass


    @abstractmethod
    def test_get_queue(self, queue_task):
        pass


    @abstractmethod
    def test_globalize(self, queue_task):
        pass


    @abstractmethod
    def test_init_queue_with_value(self, queue_task):
        pass


    @abstractmethod
    def test_async_init_queue_with_value(self, queue_task):
        pass


# @pytest.mark.usefixtures("queue_task")
class TestQueueTask(QueueTaskTestCases):

    def test_name_operator(self, queue_task: QueueTask):
        queue_task.name = _Testing_Queue_Task_Name
        _queue_task_name = queue_task.name
        assert _queue_task_name == _Testing_Queue_Task_Name, f"The queue task name should be {_Testing_Queue_Task_Name}."


    def test_queue_type_operator(self, queue_task: QueueTask):
        queue_task.queue_type = _Testing_Queue_Task_Type
        _queue_task_type = queue_task.queue_type
        assert _queue_task_type == _Testing_Queue_Task_Type, f"The queue task type should be {_Testing_Queue_Task_Type}."


    def test_value_operator(self, queue_task: QueueTask):
        queue_task.value = _Testing_Queue_Task_Value
        _queue_task_value = queue_task.value
        assert _queue_task_value == _Testing_Queue_Task_Value, f"The queue task value should be {_Testing_Queue_Task_Value}."


    def test_get_queue(self, queue_task: QueueTask):
        queue_task.name = _Testing_Queue_Task_Name
        queue_task.queue_type = _Testing_Queue_Task_Type
        _queue = queue_task.get_queue()

        _test_value = "This_is_testing_value"
        try:
            _queue.put(_test_value)
        except Exception as e:
            assert e is None, f"Occur something unexpected error. Testing fail."
        else:
            assert True, f"This object has attribute 'put' and could save value '{_test_value}'."

        try:
            _value = _queue.get()
        except Exception as e:
            assert e is None, f"Occur something unexpected error. Testing fail."
        else:
            assert True, f"This object has attribute 'get' and could get value '{_value}'."
            assert _value == _test_value, f"Value should be same as '{_test_value}' we appointed."


    def test_globalize(self, queue_task: QueueTask):
        queue_task.name = _Testing_Global_Queue_Task_Name
        queue_task.queue_type = _Testing_Queue_Task_Type
        queue_task.value = _Testing_Queue_Task_Value
        _queue = queue_task.get_queue()
        queue_task.globalize(obj=_queue)

        from multirunnable.api.manage import Running_Queue
        _queue_task_name = queue_task.name
        assert _queue_task_name in Running_Queue.keys(), f"Global value 'Running_Queue' should be have queue name '{_queue_task_name}'."
        assert Running_Queue[_queue_task_name] is not None, f"The queue value in global value should not be empty (None value) with name '{_queue_task_name}'."


    def test_init_queue_with_value(self, queue_task: QueueTask):
        queue_task.name = _Testing_Queue_Task_Name
        queue_task.queue_type = _Testing_Queue_Task_Type
        queue_task.value = _Testing_Queue_Task_Value
        queue_task.init_queue_with_values()

        from multirunnable.api.manage import Running_Queue
        _queue_task_name = queue_task.name
        assert _queue_task_name in Running_Queue.keys(), f"Global value 'Running_Queue' should be have queue name '{_queue_task_name}'."
        _under_test_queue = Running_Queue[_queue_task_name]
        assert _under_test_queue is not None, f"The queue value in global value should not be empty (None value) with name '{_queue_task_name}'."
        _queue_one_value = _under_test_queue.get()
        assert _queue_one_value is not None, f"The queue value should not be empty (None value)."


    def test_async_init_queue_with_value(self, queue_task):
        pass
        # _queue_task.async_init_queue_with_values()


