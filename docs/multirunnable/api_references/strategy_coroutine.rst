=============================
Runnable Strategy - Coroutine
=============================

*module* multirunnable.coroutine

    This subpackage responses of every features related with how to run in Coroutine.

Every running strategy or feature modules in *MultiRunnable* is an adapter which dispatches to
call the Python package which truly implements parallelism features like *multiprocessing* or *threading*.
Therefore, subpackage *multirunable.coroutine*  uses `gevent <http://www.gevent.org/>`_ (*GreenThread* modules)
and `asyncio <https://docs.python.org/3/library/asyncio.html>`_ (*Asynchronous* modules) to
implement strategy module and feature module.


Green Thread Strategy
======================

*class* multirunnable.coroutine.strategy.\ **GreenThreadStrategy**

    A generally runnable strategy object which controls runnable object. For *RunningMode.GreenThread*, it controls green threads.
    This class is an adapter of object `gevent.Greenlet <https://www.gevent.org/api/gevent.greenlet.html>`_.


**initialization**\ *(queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None, features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None, *args, **kwargs)*

    Initialing something before instantiating and running green threads.


*overload* **start_new_worker**\ *(target: Callable, args: Tuple = (), kwargs: Dict = {})*

    Instantiating and running green threads.
    Its logic is equal to instantiating *gevent.greenlet.Greenlet* and calling function *run*.


*overload* **start_new_worker**\ *(target: List[Callable], args: Tuple = (), kwargs: Dict = {})*

    Instantiating and running green threads.


**generate_worker**\ *(target: Callable, *args, **kwargs)*

    Instantiating green threads.
    Its logic is equal to instantiating *gevent.greenlet.Greenlet*.


*overload* **activate_workers**\ *(workers: Greenlet)*

    Running green threads.
    Its logic is equal to calling function *run*.


*overload* **activate_workers**\ *(workers: List[Greenlet])*

    Running green threads.


*overload* **close**\ *(workers: Greenlet)*

    Close green threads.
    Its logic is equal to calling function *join*.


*overload* **close**\ *(workers: List[Greenlet])*

    Close green threads.


**kill**\ *()*

    No support this feature.

    It is deprecated in version 0.16.0 and removed in version 0.17.0.


**get_result**\ *()*

    Get the result data of the running task in coroutine. It returns a List type value and all the element in it
    is a *MRResult* type object.


GreenThreadStrategy Pool Strategy
=================================

*class* multirunnable.coroutine.strategy.\ **GreenThreadPoolStrategy**

    A pooled strategy class which controls a pool of runnable objects. For *RunningMode.GreenThread*, it controls pool of green threads.
    This class is an adapter of object `gevent.pool.Pool <https://www.gevent.org/api/gevent.pool.html>`_.
    And the feature of mostly APIs of this class is the same as *gevent.pool.Pool*.
    So below only recording some functions which is different or new.


**initialization**\ *(queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None, features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None, *args, **kwargs)*

    The initialization before run in coroutine. It also initials features or queues here.


**map_by_args**\ *(function: Callable, args_iter: IterableType[IterableType] = (), chunksize: int = None)*

    It doesn't support the feature like *startmap* of *multiprocessing.pool.Pool* in *gevent.pool.Pool*.
    *MultiRunnable* implement this base on *map* of *gevent.pool.Pool*.
    It does the same thing as *starmap* of *multiprocessing.pool.Pool*.


**async_map_by_args**\ *(function: Callable, args_iter: IterableType[IterableType] = (), chunksize: int = None, callback: Callable = None, error_callback: Callable = None)*

    Mostly same as *map_by_args* but it's asynchronous.


**close**\ *()*

    It call methods *close* and *join* in object *gevent.pool.Pool*.


**terminal**\ *()*

    No support this feature.


**get_result**\ *()*

    Get the result data of the running task in coroutine. It returns a List type value and all the element in it
    is a *PoolResult* type object.


Asynchronous Strategy
======================

*class* multirunnable.coroutine.strategy.\ **AsynchronousStrategy**

    A generally runnable strategy object which controls runnable object. For *RunningMode.Asynchronous*, it controls asynchronous task.
    This class is an adapter of object `asyncio.tasks.Task <https://docs.python.org/3/library/asyncio-task.html>`_.


*coroutine* **initialization**\ *(queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None, features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None, *args, **kwargs)*

    Initialing something before instantiating and running asynchronous tasks.


*coroutine* *overload* **start_new_worker**\ *(target: Callable, args: Tuple = (), kwargs: Dict = {})*

    Instantiating and running asynchronous tasks.
    Its logic is equal to instantiating *multiprocessing.Process* and calling function *run*.


*coroutine* *overload* **start_new_worker**\ *(target: List[Callable], args: Tuple = (), kwargs: Dict = {})*

    Instantiating and running asynchronous tasks.


**generate_worker**\ *(target, *args, **kwargs)*

    Instantiating asynchronous tasks.
    Its logic is equal to instantiating *multiprocessing.Process*.


*coroutine* *overload* **activate_workers**\ *(workers: Task)*

    Running asynchronous tasks.
    Its logic is equal to calling function *run*.


*coroutine* *overload* **activate_workers**\ *(workers: List[Task])*

    Running asynchronous tasks.


*coroutine* *overload* **close**\ *(workers: Task)*

    No support this feature.


*coroutine* *overload* **close**\ *(workers: List[Task])*

    No support this feature.


**get_result**\ *()*

    Get the result data of the running task in coroutine. It returns a List type value and all the element in it
    is a *MRResult* type object.

