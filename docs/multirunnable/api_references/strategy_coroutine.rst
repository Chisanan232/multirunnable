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

    Parameters:
        * *executors* (int) : The count of **Greenlet** it would use.
    Return:
        **GreenThreadStrategy** object.


    **initialization**\ *(queue_tasks=None, features=None, *args, **kwargs)*

        Initialing something before instantiating and running green threads.

        Parameters:
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
            * *args & kwargs* (tuple & dict) : The argument of initial function. This option may be deprecated in version 0.18.0 or 0.19.0.
        Return:
            None


    *overload* **start_new_worker**\ *(target, args= (), kwargs={})*

        Instantiating and running green threads.
        Its logic is equal to instantiating *gevent.greenlet.Greenlet* and calling function *run*.

        Parameters:
            * *target* (Union(FunctionType, MethodType, PartialFunction)) : The target function.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A **Greenlet** object.


    *overload* **start_new_worker**\ *(target, args=(), kwargs={})*

        Instantiating and running green threads.

        Parameters:
            * *target* (List[Callable]) : A list of target functions.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A list of **Greenlet** objects.


    **generate_worker**\ *(target, *args, **kwargs)*

        Instantiating green threads.
        Its logic is equal to instantiating *gevent.greenlet.Greenlet*.

        Parameters:
            * *target* (Callable) : The target functions.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A **Greenlet** object.


    *overload* **activate_workers**\ *(workers)*

        Running green threads.
        Its logic is equal to calling function *run*.

        Parameters:
            * *workers* (Greenlet) : A **Greenlet** object.
        Return:
            None


    *overload* **activate_workers**\ *(workers)*

        Running green threads.

        Parameters:
            * *workers* (List[Greenlet]) : A list of **Greenlet** objects.
        Return:
            None


    *overload* **close**\ *(workers)*

        Close green threads.
        Its logic is equal to calling function *join*.

        Parameters:
            * *workers* (Greenlet) : A **Greenlet** object.
        Return:
            None


    *overload* **close**\ *(workers)*

        Close green threads.

        Parameters:
            * *workers* (List[Greenlet]) : A list of **Greenlet** objects.
        Return:
            None


    **kill**\ *()*

        No support this feature in currently version.

        Evaluating.

        Return:
            None


    **get_result**\ *()*

        Get the result data of the running task in coroutine. It returns a List type value and all the element in it
        is a *MRResult* type object.

        Return:
            A list of *CoroutineResult* object.


GreenThreadStrategy Pool Strategy
=================================

*class* multirunnable.coroutine.strategy.\ **GreenThreadPoolStrategy**

    A pooled strategy class which controls a pool of runnable objects. For *RunningMode.GreenThread*, it controls pool of green threads.
    This class is an adapter of object `gevent.pool.Pool <https://www.gevent.org/api/gevent.pool.html>`_.
    And the feature of mostly APIs of this class is the same as *gevent.pool.Pool*.
    So below only recording some functions which is different or new.

    Parameters:
        * *pool_size* (int) : The size of pool which would preprocessing about initialing **Greenlet**.
    Return:
        **GreenThreadPoolStrategy** object.


    **initialization**\ *(queue_tasks=None, features=None, *args, **kwargs)*

        The initialization before run in coroutine. It also initials features or queues here.

        Parameters:
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
            * *args & kwargs* (tuple & dict) : The argument of initial function. This option may be deprecated in version 0.18.0 or 0.19.0.
        Return:
            None


    **map_by_args**\ *(function, args_iter=(), chunksize=None)*

        It doesn't support the feature like *startmap* of *multiprocessing.pool.Pool* in *gevent.pool.Pool*.
        *MultiRunnable* implement this base on *map* of *gevent.pool.Pool*.
        It does the same thing as *starmap* of *multiprocessing.pool.Pool*.

        Parameters:
            * *function* (Callable) : The target function.
            * *args_iter* (IterableType[IterableType]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
            * *chunksize* (int) : No working currently.
        Return:
            None


    **async_map_by_args**\ *(function, args_iter=(), chunksize=None, callback=None, error_callback=None)*

        This function is asynchronous version of *map_by_args*.

        Parameters:
            * *function* (Callable) : The target function.
            * *args_iter* (IterableType[IterableType]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
            * *chunksize* (int) : No working currently.
            * *callback* (Callable) : The callback function which would be run after the target function run successfully without any issues.
            * *error_callback* (Callable) : The callback function which would be run when it raising any exception or error.
        Return:
            None


    **close**\ *()*

        It call methods *close* and *join* in object *gevent.pool.Pool*.

        Return:
            None


    **terminal**\ *()*

        No support this feature.

        Return:
            None


    **get_result**\ *()*

        Get the result data of the running task in coroutine. It returns a List type value and all the element in it
        is a *PoolResult* type object.

        Return:
            A list of *GreenThreadPoolResult* object.


Asynchronous Strategy
======================

*class* multirunnable.coroutine.strategy.\ **AsynchronousStrategy**

    A generally runnable strategy object which controls runnable object. For *RunningMode.Asynchronous*, it controls asynchronous task.
    This class is an adapter of object `asyncio.tasks.Task <https://docs.python.org/3/library/asyncio-task.html>`_.

    Parameters:
        * *executors* (int) : The count of **Task** it would use.
    Return:
        **AsynchronousStrategy** object.


    *coroutine* **initialization**\ *(queue_tasks=None, features=None, *args, **kwargs)*

        Initialing something before instantiating and running asynchronous tasks.

        Parameters:
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
            * *args & kwargs* (tuple & dict) : The argument of initial function. This option may be deprecated in version 0.18.0 or 0.19.0.
        Return:
            None


    *coroutine* *overload* **start_new_worker**\ *(target, args=(), kwargs={})*

        Instantiating and running asynchronous tasks.
        Its logic is equal to instantiating *multiprocessing.Greenlet* and calling function *run*.

        Parameters:
            * *target* (Union(FunctionType, MethodType, PartialFunction)) : The target function.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A **Task** object.


    *coroutine* *overload* **start_new_worker**\ *(target, args=(), kwargs={})*

        Instantiating and running asynchronous tasks.

        Parameters:
            * *target* (List[Callable]) : A list of target functions.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A list of **Task** objects.


    **generate_worker**\ *(target, *args, **kwargs)*

        Instantiating asynchronous tasks.
        Its logic is equal to instantiating *asyncio.create_task*.

        Parameters:
            * *target* (Callable) : The target functions.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            A **Task** object.


    *coroutine* *overload* **activate_workers**\ *(workers)*

        Running asynchronous tasks.
        Its logic is equal to calling function *run*.

        Parameters:
            * *workers* (Task) : A **Task** object.
        Return:
            None


    *coroutine* *overload* **activate_workers**\ *(workers)*

        Running asynchronous tasks.

        Parameters:
            * *workers* (List[Task]) : A list of **Task** objects.
        Return:
            None


    *coroutine* *overload* **close**\ *(workers)*

        No support this feature.

        Parameters:
            * *workers* (Task) : A **Task** object.
        Return:
            None


    *coroutine* *overload* **close**\ *(workers)*

        No support this feature.

        Parameters:
            * *workers* (List[Task]) : A list of **Task** objects.
        Return:
            None


    **get_result**\ *()*

        Get the result data of the running task in coroutine. It returns a List type value and all the element in it
        is a *MRResult* type object.

        Return:
            A list of *AsynchronousResult* object.

