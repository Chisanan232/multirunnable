============================
Runnable Strategy - Parallel
============================

*module* multirunnable.parallel

    This subpackage responses of every features related with how to run in Parallel.

Every running strategy or feature modules in *MultiRunnable* is an adapter which dispatches to
call the Python package which truly implements parallelism features like *multiprocessing* or *threading*.
Therefore, subpackage *multirunable.parallel*  uses `multiprocessing <https://docs.python.org/3/library/multiprocessing.html>`_ to implement strategy module and feature module.


Process Strategy
==================

*class* multirunnable.parallel.strategy.\ **ProcessStrategy**

    A generally runnable strategy object which controls runnable object. For *RunningMode.Parallel*, it controls processes.
    This class is an adapter of object `multiprocessing.Process <https://docs.python.org/3/library/multiprocessing.html#process-and-exceptions>`_.


**initialization**\ *(queue_tasks, features, *args, **kwargs)*

    Initialing something before instantiating and running Processes.


*overload* **start_new_worker**\ *(target: (FunctionType, MethodType, PartialFunction), args, kwargs)*

    Instantiating and running Processes.
    Its logic is equal to instantiating *multiprocessing.Process* and calling function *run*.


*overload* **start_new_worker**\ *(target: Iterable, args, kwargs)*

    Instantiating and running Processes.


**generate_worker**\ *(target, *args, **kwargs)*

    Instantiating Processes.
    Its logic is equal to instantiating *multiprocessing.Process*.


*overload* **activate_workers**\ *(workers: Process)*

    Running Processes.
    Its logic is equal to calling function *run*.


*overload* **activate_workers**\ *(workers: Iterable)*

    Running Processes.


*overload* **close**\ *(workers: Process)*

    Close Processes.
    Its logic is equal to calling function *join* and *close* (calling *join* only in Python 3.6).


*overload* **close**\ *(workers: Iterable)*

    Close Processes.


**terminal**\ *()*

    Terminate Processes.
    Its logic is equal to function *terminal* in object *multiprocessing.Process*.


**kill**\ *()*

    Kill Processes.
    Its logic is equal to function *kill* in object *multiprocessing.Process*.


**get_result**\ *()*

    Get the result data of the running task in parallel. It returns a List type value and all the element in it
    is a *MRResult* type object.


Process Pool Strategy
======================

*class* multirunnable.parallel.strategy.\ **ProcessPoolStrategy**

    A pooled strategy class which controls a pool of runnable objects. For *RunningMode.Parallel*, it controls pool of processes.
    This class is an adapter of object `multiprocessing.pool.Pool <https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing.pool>`_.
    And the feature of mostly APIs of this class is the same as *multiprocessing.pool.Pool*.
    So below only recording some functions which is different or new.


**initialization**\ *(queue_tasks, features, *args, **kwargs)*

    The initialization before run in parallel. It also initials features or queues here.


**close**\ *()*

    It call methods *close* and *join* in object *multiprocessing.pool.Pool*.


**get_result**\ *()*

    Get the result data of the running task in parallel. It returns a List type value and all the element in it
    is a *PoolResult* type object.

