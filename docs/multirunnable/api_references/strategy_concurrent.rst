==============================
Runnable Strategy - Concurrent
==============================

*module* multirunnable.concurrent

    This subpackage responses of every features related with how to run in Concurrent.

Every running strategy or feature modules in *MultiRunnable* is an adapter which dispatches to
call the Python package which truly implements parallelism features like *multiprocessing* or *threading*.
Therefore, subpackage *multirunable.concurrent*  uses `threading <https://docs.python.org/3/library/threading.html>`_ (*GeneralStrategy*)
or `multiprocessing <https://docs.python.org/3/library/threading.html>`_ (*PoolStrategy*) to implement strategy module and feature module.


Thread Strategy
================

*class* multirunnable.concurrent.strategy.\ **ThreadStrategy**

    A generally runnable strategy object which controls runnable object. For *RunningMode.Concurrent*, it controls processes.
    This class is an adapter of object `threading.Thread <https://docs.python.org/3/library/threading.html#thread-objects>`_.

    Parameters:
        * *executors* (int) : The count of **Thread** it would use.
    Return:
        **ThreadStrategy** object.


    **initialization**\ *(queue_tasks=None, features=None, *args, **kwargs)*

        Initialing something before instantiating and running Threads.

        Parameters:
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
            * *args & kwargs* (tuple & dict) : The argument of initial function. This option may be deprecated in version 0.18.0 or 0.19.0.
        Return:
            None


    *overload* **start_new_worker**\ *(target, args, kwargs)*

        Instantiating and running Threads.
        Its logic is equal to instantiating *threading.Thread* and calling function *run*.

        Parameters:
            * *target* (Union(FunctionType, MethodType, PartialFunction)) : The target function.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A **Thread** object.


    *overload* **start_new_worker**\ *(target, args, kwargs)*

        Instantiating and running Threads.

        Parameters:
            * *target* (List[Callable]) : A list of target functions.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A list of **Thread** objects.


    **generate_worker**\ *(target, *args, **kwargs)*

        Instantiating Threads.
        Its logic is equal to instantiating *threading.Thread*.

        Parameters:
            * *target* (Callable) : The target functions.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A **Thread** object.


    *overload* **activate_workers**\ *(workers)*

        Running Threads.
        Its logic is equal to calling function *run*.

        Parameters:
            * *workers* (Thread) : A **Thread** object.
        Return:
            None


    *overload* **activate_workers**\ *(workers)*

        Running Threads.

        Parameters:
            * *workers* (List[Thread]) : A list of **Thread** objects.
        Return:
            None


    *overload* **close**\ *(workers)*

        Close Threads.
        Its logic is equal to calling function *join*.

        Parameters:
            * *workers* (Thread) : A **Thread** object.
        Return:
            None


    *overload* **close**\ *(workers)*

        Close Threads.

        Parameters:
            * *workers* (List[Thread]) : A list of **Thread** objects.
        Return:
            None


    **get_result**\ *()*

        Get the result data of the running task in parallel. It returns a List type value and all the element in it
        is a *MRResult* type object.

        Return:
            A list of *MRResult* object.


Thread Pool Strategy
=====================

*class* multirunnable.concurrent.strategy.\ **ThreadPoolStrategy**

    A pooled strategy class which controls a pool of runnable objects. For *RunningMode.Concurrent*, it controls pool of processes.
    This class is an adapter of object `multiprocessing.pool.ThreadPool <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.ThreadPool>`_.
    And the feature of mostly APIs of this class is the same as *multiprocessing.pool.ThreadPool*.
    So below only recording some functions which is different or new.

    Parameters:
        * *pool_size* (int) : The size of pool which would preprocessing about initialing **Thread**.
    Return:
        **ThreadPoolStrategy** object.


    **initialization**\ *(queue_tasks=None, features=None, *args, **kwargs)*

        The initialization before run in concurrent. It also initials features or queues here.

        Parameters:
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
            * *args & kwargs* (tuple & dict) : The argument of initial function. This option may be deprecated in version 0.18.0 or 0.19.0.
        Return:
            None


    **close**\ *()*

        It call methods *close* and *join* in object *multiprocessing.pool.ThreadPool*.

        Return:
            None


    **get_result**\ *()*

        Get the result data of the running task in parallel. It returns a List type value and all the element in it
        is a *PoolResult* type object.

        Return:
            A list of *ThreadPoolStrategy* object.
