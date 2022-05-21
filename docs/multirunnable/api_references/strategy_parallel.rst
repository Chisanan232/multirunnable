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

    Parameters:
        * *executors* (int) : The count of **Process** it would use.
    Return:
        **ProcessStrategy** object.


    **initialization**\ *(queue_tasks=None, features=None, *args, **kwargs)*

        Initialing something before instantiating and running Processes.

        Parameters:
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
            * *args & kwargs* (tuple & dict) : The argument of initial function. This option may be deprecated in version 0.18.0 or 0.19.0.
        Return:
            None


    *overload* **start_new_worker**\ *(target, args=(), kwargs={})*

        Instantiating and running Processes.
        Its logic is equal to instantiating *multiprocessing.Process* and calling function *run*.

        Parameters:
            * *target* (Union(FunctionType, MethodType, PartialFunction)) : The target function.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A **Process** object.


    *overload* **start_new_worker**\ *(target, args=(), kwargs={})*

        Instantiating and running Processes.

        Parameters:
            * *target* (List[Callable]) : A list of target functions.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A list of **Process** objects.


    **generate_worker**\ *(target: Callable, *args, **kwargs)*

        Instantiating Processes.
        Its logic is equal to instantiating *multiprocessing.Process*.

        Parameters:
            * *target* (Callable) : The target functions.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A **Process** object.


    *overload* **activate_workers**\ *(workers)*

        Running Processes.
        Its logic is equal to calling function *run*.

        Parameters:
            * *workers* (Process) : A **Process** object.
        Return:
            None


    *overload* **activate_workers**\ *(workers)*

        Running Processes.

        Parameters:
            * *workers* (List[Process]) : A list of **Process** objects.
        Return:
            None


    *overload* **close**\ *(workers: Process)*

        Close Processes.
        Its logic is equal to calling function *join* and *close* (calling *join* only in Python 3.6).

        Parameters:
            * *workers* (Process) : A **Process** object.
        Return:
            None


    *overload* **close**\ *(workers: List[Process])*

        Close Processes.

        Parameters:
            * *workers* (List[Process]) : A list of **Process** objects.
        Return:
            None


    **terminal**\ *()*

        Terminate Processes.
        Its logic is equal to function *terminal* in object *multiprocessing.Process*.

        Return:
            None


    **kill**\ *()*

        Kill Processes.
        Its logic is equal to function *kill* in object *multiprocessing.Process*.

        Return:
            None


    **get_result**\ *()*

        Get the result data of the running task in parallel. It returns a List type value and all the element in it
        is a *MRResult* type object.

        Return:
            A list of *ParallelResult* object.


Process Pool Strategy
======================

*class* multirunnable.parallel.strategy.\ **ProcessPoolStrategy**

    A pooled strategy class which controls a pool of runnable objects. For *RunningMode.Parallel*, it controls pool of processes.
    This class is an adapter of object `multiprocessing.pool.Pool <https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing.pool>`_.
    And the feature of mostly APIs of this class is the same as *multiprocessing.pool.Pool*.
    So below only recording some functions which is different or new.

    Parameters:
        * *pool_size* (int) : The size of pool which would preprocessing about initialing **Process**.
    Return:
        **ProcessPoolStrategy** object.


    **initialization**\ *(queue_tasks=None, features=None, *args, **kwargs)*

        The initialization before run in parallel. It also initials features or queues here.

        Parameters:
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
            * *args & kwargs* (tuple & dict) : The argument of initial function. This option may be deprecated in version 0.18.0 or 0.19.0.
        Return:
            None


    **close**\ *()*

        It call methods *close* and *join* in object *multiprocessing.pool.Pool*.

        Return:
            None


    **get_result**\ *()*

        Get the result data of the running task in parallel. It returns a List type value and all the element in it
        is a *PoolResult* type object.

        Return:
            A list of *ProcessPoolResult* object.

