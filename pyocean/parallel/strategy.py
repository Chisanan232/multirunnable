from pyocean.framework.strategy import RunnableStrategy, Resultable, Globalize as RunningGlobalize
from pyocean.framework.features import BaseQueueType
from pyocean.api.features_adapter import RunningMode, RunningStrategyAPI
from pyocean.parallel.features import MultiProcessingQueueType
from pyocean.persistence import OceanPersistence
from pyocean.persistence.database import SingleConnection, MultiConnections
from pyocean.persistence.database.multi_connections import Globalize as DatabaseGlobalize
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

    # _Running_Mode: RunningMode = RunningMode.Process
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
        # Initialize and assign task queue object.
        process_queue = self.init_tasks_queue(qtype=MultiProcessingQueueType.Queue)
        tasks_queue = self.add_task_to_queue(queue=process_queue, task=tasks)
        # Globalize object to share between different multiple processes
        RunningGlobalize.tasks_queue(tasks_queue=tasks_queue)
        print("[DEBUG] queue: ", process_queue)
        print("[DEBUG] tasks: ", tasks)

        # Initialize parameter and object with different scenario.
        # self.__init_by_strategy(tasks_queue=tasks_queue)
        pre_init_params: Dict = {}
        if isinstance(self._persistence_strategy, SingleConnection):
            # Single Connection Initialize Procedure
            # from multiprocessing import Lock
            # # pre_init_params["tasks_queue"] = tasks_queue
            # pre_init_params["limited_obj"] = Lock
            pass
        elif isinstance(self._persistence_strategy, MultiConnections):
            # Multiple Connection Initialize Procedure
            # from multiprocessing import Semaphore
            # # pre_init_params["tasks_queue"] = tasks_queue
            # pre_init_params["limited_obj"] = Semaphore
            # # pre_init_params["pool_name"] = "stock_crawler"
            pre_init_params["db_connection_instances_number"] = self.db_connection_instances_number
        elif isinstance(self._persistence_strategy, SingleFileSaver):
            # Single File Saver Initialize Procedure
            # from multiprocessing import Lock
            # # pre_init_params["tasks_queue"] = tasks_queue
            # pre_init_params["limited_obj"] = Lock
            pass
        elif isinstance(self._persistence_strategy, MultiFileSaver):
            # Multiple File Savers Initialize Procedure
            # from multiprocessing import Semaphore
            # # pre_init_params["tasks_queue"] = tasks_queue
            # pre_init_params["limited_obj"] = Semaphore
            pass
        else:
            # Unexpected scenario
            print("[DEBUG] issue ...")
            raise Exception
        # self._persistence_strategy.initialize(**pre_init_params)
        print("[DEBUG] Pre-Init process start ....")
        # self._persistence_strategy.initialize(limitation=OceanSemaphore,  mode=self._Running_Mode, **pre_init_params)
        self._persistence_strategy.initialize(mode=self._Running_Mode,  queue_type=MultiProcessingQueueType.Queue, **pre_init_params)

        # Initialize and build the Processes Pool.
        self._Processors_Pool = Pool(processes=self.threads_number, initializer=pool_initializer, initargs=pool_initargs)
        print("[DEBUG] Pre-Init process finish.")


    @deprecated(version="0.6", reason="Remove useless logic code")
    def __init_by_strategy(self, tasks_queue: Queue) -> None:
        """
        Description:
            Initialize something which be needed.

        Note:
            For every running strategy, they have something must to be initial: Lock or Semaphore, connection pool if it needs.
            And base on the persistence mode, it has different ways to save data:
            1. Multi-Worker with One Connection Instance (SingleConnection)
               one connection instance, lock
               -> Deprecated one connection instance and change to use connection pool. Deprecated lock and change to use semaphore.
               -> Reason: efficiency
            2. Multi-Worker with Multi-Connection Instances (MultiConnection)
               one connection pool which saving multiple connection instances, semaphore
            3. Multi-Worker with One file (SingleSaver-BaseFileFormatter)
               one IO instance, lock (Saving into same file)
            4. Multi-Worker with Multi-Files (MultiSaver-BaseFileFormatter)
               multiple IO instances in each process, lock (Saving into many different file)

        :param tasks_queue:
        :return:
        """
        if isinstance(self._persistence_strategy, MultiConnections):
            # # # # Multiprocessing with database connection pool
            # Initialize Processes Semaphore. (related with persistence)
            # It has 2 possible that the step has: Lock (For database - one connection instance and file) or
            # Semaphore (For database - connection pool).
            # RLock mostly like Semaphore, so doesn't do anything with RLock currently.
            process_semaphore = Semaphore(value=self.db_connection_instances_number)

            # Initialize the Database Connection Instances Pool. (related with persistence)
            database_connections_pool = self._persistence_strategy.connect_database(pool_name="stock_crawler",
                                                                                    pool_size=self.db_connection_instances_number)

            # (related with persistence)
            self.__globalize_init_object_new(tasks_queue, process_semaphore, database_connections_pool)
            # pool_initializer = self.__init_something
            # pool_initargs = (running_initializer, running_initargs, tasks_queue, process_semaphore, database_connections_pool, )

        elif isinstance(self._persistence_strategy, SingleConnection):
            # # # # Multiprocessing with oen database connection instance
            # Deprecated the method about mutiprocessing saving with one connection and change to use multiprocessing
            # saving with pool size is 1 connection pool. The reason is database instance of connection pool is already,
            # but for the locking situation, we should:
            # lock acquire -> new instance -> execute something -> close instance -> lock release . and loop and loop until task finish.
            # But connection pool would:
            # new connection instances and save to pool -> semaphore acquire -> GET instance (not NEW) ->
            # execute something -> release instance back to pool (not CLOSE instance) -> semaphore release
            from multiprocessing import Lock
            process_lock = Lock()
            # Because only one connection instance, the every process take turns to using it to saving data. In other words,
            # here doesn't need to initial anything about database connection.

            # (related with persistence)
            self.__globalize_init_object_new(tasks_queue, process_lock)
            # pool_initializer = self.__init_something
            # pool_initargs = (running_initializer, running_initargs, tasks_queue, process_lock, )

        elif isinstance(self._persistence_strategy, SingleFileSaver):
            # # # # Multiprocessing with each mapping file. So this options shouldn't be run with multiprocessing or
            # no matter use which one strategy, it would garuntee the result report is ONE file. (consider ...?)
            raise Exception("MultiProcessing running strategy shouldn't use SingleFileSaver persistence strategy. "
                            "Please select others persistence strategy.")

        elif isinstance(self._persistence_strategy, MultiFileSaver):
            # # # # Multiprocessing with multiple files to saving data and compress data finally.
            # Each processes save data as file with the stock symbol as file name, but program will distribute task by
            # stock symbol, so it's impossible that occur resources rare condition between with each different processes
            # when running.
            self.__globalize_init_object_new(tasks_queue)
            # pool_initializer = self.__init_something
            # pool_initargs = (running_initializer, running_initargs, tasks_queue, )

        else:
            raise Exception("It's impossible issue.")


    @deprecated(version="0.4", reason="Remove useless logic code")
    def __init_something(self, running_initializer: Callable = None, running_initargs: Iterable = None, *args, **kwargs):
        if running_initializer:
            running_initializer(running_initargs)
        self.__globalize_init_object_new(*args, **kwargs)


    @deprecated(version="0.6", reason="Remove useless logic code")
    def __globalize_init_object_new(self, *args, **kwargs) -> None:
        """
        Note:
            Question (?):
              Here has a bad solution about the globalize procedure be determined by string of object. it will add the
              risk about unexpected bug occur in the future.
        :param args:
        :param kwargs:
        :return:
        """
        # (related with persistence)
        for arg in args:
            print("arg: ", arg)
            if "Queue" in repr(arg):
                RunningGlobalize.tasks_queue(tasks_queue=arg)
            elif "Lock" in repr(arg):
                RunningGlobalize.lock(lock=arg)
            elif "Semaphore" in repr(arg):
                RunningGlobalize.semaphore(smp=arg)
            else:
                print("Connection Pool: ", arg)
                DatabaseGlobalize.connection_pool(pool=arg)

        if kwargs.get("pool", None):
            print("Connection Pool: ", kwargs["pool"])
            DatabaseGlobalize.connection_pool(pool=kwargs["pool"])


    @deprecated(version="0.6", reason="Remove useless logic code")
    def __globalize_init_object(self, tasks_queue: Process_Queue, semaphore: Semaphore, database_connections_pool: object) -> None:
        RunningGlobalize.semaphore(smp=semaphore)
        RunningGlobalize.tasks_queue(tasks_queue=tasks_queue)
        DatabaseGlobalize.connection_pool(pool=database_connections_pool)


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


    def init_tasks_queue(self, qtype: BaseQueueType) -> Union[Process_Queue, Queue]:
        # Older written
        # return Process_Queue()
        # New written
        __running_api = RunningStrategyAPI(mode=self._Running_Mode)
        __queue = __running_api.queue(qtype=qtype)
        return __queue


    def add_task_to_queue(self, queue: Union[Process_Queue, Queue], task: Iterable) -> Union[Process_Queue, Queue]:
        for t in task:
            queue.put(t)
        return queue


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

