===================
Executors Modules
===================

Executor modules means a unit worker of runnable like Process (Parallel), Thread (Concurrent), Green Thread (Coroutine) or Task (Asynchronous).
It would run as the runnable you set with option *mode* (:doc:`./mode`).


Executor
===========

*module* multirunnable.executor

*class*  multirunnable.executor.\ **Executor**\ *(executors)*

    An abstracted class which implement mostly all methods of class *multirunnable.framework.BaseExecutor*.
    The left one abstract method *_initial_running_strategy* which doesn't be implemented is generating running strategy.

    Parameters:
        * *mode* (RunningMode) : Be deprecated and remove in version 0.17.0.
        * *executors* (int) : The count of :ref:`worker (MultiRunnable Worker Concept)` it would use.
    Return:
        **Executor** object.


    **start_new_worker**\ *(target, args=(), kwargs={})*

        It would initial a runnable worker and run it immediately. It won't close runnable worker.

        Parameters:
            * *target* (Callable) : The target function would be run in a *Worker*.
            * *args* (Tuple) : The argument of target function. It would pass the arguments to the function via *(opt1, opt2, ...)*.
            * *kwargs* (Dict) : The argument of target function, It would pass the arguments to the function via *(param1=opt1, param2=opt2, ...)*.
        Return:
            None.


    **run**\ *(function, args=None, queue_tasks=None, features=None)*

        It would do initialing first (before instantiate runnable worker).
        It instantiates runnable workers as the mount by option *executors* and runs them.
        Finally, it would close the runnable worker.

        Parameters:
            * *function* (Callable) : The target function would be run in a *Worker*.
            * *args* (Optional[Union[Tuple, Dict]]) : The argument of target function. It could receive the type as tuple or dictionary.
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
        Return:
            None.


    **map**\ *(function, args_iter=[], queue_tasks=None, features=None)*

        Same as method *run*, but the mount of runnable workers which be created are same as mount of arguments.
        It would run as builtin function *map* with option *args_iter*.

        +------------+--------------------------------+-----------------------------------------+
        |  Iterator  |           arguments            |                 Result                  |
        +============+================================+=========================================+
        |     map    | [function, (arg1, arg2, ...)]  |   function(arg1), function(arg2), ...   |
        +------------+--------------------------------+-----------------------------------------+

        Parameters:
            * *function* (Callable) : The target function would be run in a *Worker*.
            * *args_iter* (Iterable) : An iterator of target function arguments.
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
        Return:
            None.


    **map_with_function**\ *(functions, args_iter=[], queue_tasks=None, features=None)*

        Same as method *run*, but the mount of runnable workers which be created are same as mount of functions.
        It would run the function with the mapping index of argument iterator.

        +--------------------------+----------------------------------------------------+-------------------------------------------+
        |          Iterator        |                     arguments                      |                  Result                   |
        +==========================+====================================================+===========================================+
        |     map_with_function    |  [(function1, function2, ...), (arg1, arg2, ...)]  |   function1(arg1), function2(arg2), ...   |
        +--------------------------+----------------------------------------------------+-------------------------------------------+

        Parameters:
            * *functions* (Iterable[Callable]) : An iterator of target functions would be run in *Workers*.
            * *args_iter* (Iterable) : An iterator of target function arguments.
            * *queue_tasks* (Optional[Union[BaseQueueTask, BaseList]]) : Initial the QueueTask so that it could operate the queue in the parallelism.
            * *features* (Optional[Union[BaseFeatureAdapterFactory, BaseList]]) : Initial the synchronization feature object so that it could operate the synchronization in parallelism.
        Return:
            None.


    **close**\ *(workers)*

        Close the resource of runnable worker(s).

        Parameters:
            * *workers* (Union[_MRTasks, List[_MRTasks]]) : An iterator of *Workers*.
        Return:
            None.


    **result**\ *()*

        Get the return values which be returned by function of runnable workers. It would
        raise a ValueError if the current strategy object isn't a *Resultable* object.

        Will deprecate and remove in version 0.18.0. Change to be a protected function
        and be called in methods *start_new_worker*, *run*, *map* and *map_with_function*.

        Return:
            A List[MRResult] object.



SimpleExecutor
================

*module* multirunnable.executor

*class*  multirunnable.executor.\ **SimpleExecutor**\ *(executors, mode=None)*

    An *Executor* object which could build parallelism as Parallel, Concurrent or Coroutine via option *mode*.

    Parameters:
        * *mode* (Optional[RunningMode]) : Which *RunningMode* choice to use.
        * *executors* (int) : The count of :ref:`worker (MultiRunnable Worker Concept)` it would use.
    Return:
        **Executor** object.


    **_initial_running_strategy**\ *()*

        Initial running strategy object which executor uses. The running
        strategy be controlled by option *mode*.

        Return:
            None.



AdapterExecutor
=================

*module* multirunnable.executor

*class*  multirunnable.executor.\ **AdapterExecutor**\ *(strategy=None)*

    An *Executor* object which could build parallelism with customized features as Parallel, Concurrent or Coroutine via option *strategy*.

    Parameters:
        * *strategy* (Union[GeneralRunnableStrategy]) : The customized running strategy object which be extends *multirunnable.framework.runnable.GeneralRunnableStrategy* and implements all methods.
    Return:
        **Executor** object.


    **_initial_running_strategy**\ *()*

        Initial running strategy object which executor uses. It would annotate the global
        variable *General_Runnable_Strategy* with the strategy object it gets from parameter
        *strategy*.

        Return:
            None.

