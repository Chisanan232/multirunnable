from pyocean.framework.strategy import InitializeUtils, RunnableStrategy, Resultable, Globalize as RunningGlobalize
from pyocean.framework.features import BaseQueueType
from pyocean.api import RunningMode, RunningStrategyAPI
from pyocean.parallel.features import MultiProcessingQueueType
from pyocean.persistence import OceanPersistence
from pyocean.persistence.database import SingleConnection, MultiConnections
from pyocean.persistence.file.saver import BaseFileSaver, SingleFileSaver, MultiFileSaver

from abc import abstractmethod
from multiprocessing import Pool, Manager, Lock, Semaphore, Queue as Process_Queue
from multiprocessing.managers import Namespace
from multiprocessing.pool import Pool, AsyncResult, ApplyResult
from threading import Thread
from queue import Queue
from typing import List, Tuple, Dict, Iterable, Union, Callable, cast
from deprecated.sphinx import deprecated
import re



class ParallelStrategy(RunnableStrategy):

    _Running_Mode: RunningMode = RunningMode.MultiProcessing
    _Manager: Manager = None
    _Namespace_Object: Namespace = None
    _Processors_Pool: Pool = None
    _Processors_Running_Result: Dict[str, Dict[str, Union[AsyncResult, bool]]] = {}

    def __init__(self, persistence_strategy: OceanPersistence, threads_num: int, db_connection_pool_size: int = None):
        """
        Description:
            Converting the object to multiprocessing.manager.Namespace type object at initial state.
        :param persistence_strategy:
        :param threads_num:
        :param db_connection_pool_size:
        """
        self.__init_namespace_obj()
        namespace_persistence_strategy = cast(OceanPersistence, self.__namespacing_instance(instance=persistence_strategy))
        super().__init__(persistence_strategy=namespace_persistence_strategy,
                         threads_num=threads_num,
                         db_connection_pool_size=db_connection_pool_size)
        self._Processors_Running_Result = self._Manager.dict()


    def __init_namespace_obj(self) -> None:
        self._Manager = Manager()
        self._Namespace_Object = self._Manager.Namespace()


    def __namespacing_instance(self, instance: object) -> object:
        setattr(self._Namespace_Object, repr(instance), instance)
        return getattr(self._Namespace_Object, repr(instance))


    @deprecated(version="0.1", reason="The code looks be useless method currently.")
    @abstractmethod
    def namespacilize_object(self, objects: Iterable[object]) -> Namespace:
        """
        Description:
              Set the object which be shared to use between multiple processes as MultiProcessing NameSpace object to
              reach shared object requirement.
        :param objects:
        :return:
        """
        pass



class MultiProcessingStrategy(ParallelStrategy, Resultable):

    def init_multi_working(self,
                           tasks: Iterable,
                           pool_initializer: Callable = None,
                           pool_initargs: Iterable = None,
                           *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # Initialize and assign task queue object.
        __init_utils.initialize_queue(tasks=tasks, qtype=MultiProcessingQueueType.Queue)
        # Initialize parameter and object with different scenario.
        __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_instances_number)

        # Initialize and build the Processes Pool.
        self._Processors_Pool = Pool(processes=self.threads_number, initializer=pool_initializer, initargs=pool_initargs)
        print("[DEBUG] Pre-Init process finish.")


    def namespacilize_object(self, objects: Iterable[Callable]) -> Namespace:
        """
        Note:
            It's possible that occur some unexpected issue if the entry value isn't class instance.
        Question:
            Should fix the issue about it cannot assign object instance correctly.
        """

        for obj in objects:
            if not isinstance(obj, Callable):
                raise TypeError("The object element of List isn't Callable.")

        __common_objects = self._Manager.Namespace()
        instance_dict = {}
        for obj in objects:
            __instance_name = self.__parse_class_name(object_char=obj)
            instance_dict[__instance_name] = obj
            # __common_objects.Common_Objects_Dict.common_objects[__instance_name] = obj

        __common_objects.Common_Objects_Dict = instance_dict
        return __common_objects


    def __parse_class_name(self, object_char: object) -> str:
        """
        Description:
            Parse the object package and class name.
        :param object_char:
        :return:
        """

        if re.search(r"<class \'\w{0,64}\.\w{0,64}\'>", str(object_char), re.IGNORECASE) is None:
            raise Exception("Cannot parse the class instance string")
        return str(object_char).split(".")[-1].split("'>")[0]


    @deprecated(version="0.8", reason="Move the method up to super-class 'RunnableStrategy'")
    def initialize_queue(self, tasks: Iterable, qtype: BaseQueueType):
        __queue = self.init_tasks_queue(qtype=qtype)
        __tasks_queue = self.add_task_to_queue(queue=__queue, task=tasks)
        RunningGlobalize.queue(queue=__tasks_queue)


    @deprecated(version="0.8", reason="Move the method up to super-class 'RunnableStrategy'")
    def init_tasks_queue(self, qtype: BaseQueueType) -> Union[Process_Queue, Queue]:
        __running_api = RunningStrategyAPI(mode=self._Running_Mode)
        __queue = __running_api.queue(qtype=qtype)
        return __queue


    @deprecated(version="0.8", reason="Move the method up to super-class 'RunnableStrategy'")
    def add_task_to_queue(self, queue: Union[Process_Queue, Queue], task: Iterable) -> Union[Process_Queue, Queue]:
        for t in task:
            queue.put(t)
        return queue


    @deprecated(version="0.8", reason="Move the method up to super-class 'RunnableStrategy'")
    def initialize_persistence(self):
        pre_init_params: Dict = {}
        if isinstance(self._persistence_strategy, SingleConnection):
            pass
        elif isinstance(self._persistence_strategy, MultiConnections):
            pre_init_params["db_connection_instances_number"] = self.db_connection_instances_number
        elif isinstance(self._persistence_strategy, SingleFileSaver):
            pass
        elif isinstance(self._persistence_strategy, MultiFileSaver):
            pass
        else:
            # Unexpected scenario
            print("[DEBUG] issue ...")
            raise Exception
        print("[DEBUG] Pre-Init process start ....")
        self._persistence_strategy.initialize(mode=self._Running_Mode, **pre_init_params)


    def build_multi_workers(self,
                            function: Callable,
                            args: Tuple = (),
                            kwargs: Dict = {},
                            callback: Callable = None,
                            error_callback: Callable = None) -> List[Union[Thread, ApplyResult]]:
        return [self._Processors_Pool.apply_async(func=function,
                                                  args=args,
                                                  kwds=kwargs,
                                                  callback=callback,
                                                  error_callback=error_callback)
                for _ in range(self.threads_number)]
        # elif kwargs:
        #     return [self._Processors_Pool.apply_async(func=function, kwds=kwargs, callback=callaback, error_callback=error_callback)
        #             for _ in range(self.threads_number)]


    def activate_worker(self, worker: Union[Thread, ApplyResult]) -> None:
        __process_running_result = worker.get()
        __process_run_successful = worker.successful()

        # __process_memory_addr = str(worker).split("at")[-1]
        __process_pid = f"process_{__process_running_result['pid']}"
        # Save Running result state and Running result value as dict
        process_result = {"successful": __process_run_successful, "result": __process_running_result}
        # Initial and saving value
        self._Processors_Running_Result[__process_pid] = process_result


    def end_multi_working(self) -> None:
        print("Close multi-Process ...")
        self._Processors_Pool.close()
        self._Processors_Pool.join()
        print("Close !")


    def get_multi_working_result(self) -> Iterable[object]:
        print(f"[DEBUG] self._Processors_Running_Result: {self._Processors_Running_Result}")
        return self._Processors_Running_Result

