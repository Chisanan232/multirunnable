===================
Executors Modules
===================

Executor modules means a unit worker of runnable like Process (Parallel), Thread (Concurrent), Green Thread (Coroutine) or Task (Asynchronous).
It would run as the runnable you set with option *mode* (:doc:`./mode`).


Executor
===========

*module* multirunnable.executor

*class*  multirunnable.executor.\ **Executor**\ *(executors: int)*

    An abstracted class which implement mostly all methods. The left one abstract
    method *_initial_running_strategy* is generating running strategy with option *mode*.

    About️ option *mode* and *executors*, it will be deprecated in version 0.17.0.


**start_new_worker**\ *(target: Callable, args: Tuple = (), kwargs: Dict = {})*

    It would initial a runnable worker and run it immediately. It won't close runnable worker.


**run**\ *(function: CallableType, args: Optional[Union[Tuple, Dict]] = None, queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None, features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None)*

    It would do initialing first (before instantiate runnable worker).
    It instantiates runnable workers as the mount by option *executors* and runs them.
    It would close the runnable worker finally.


**map**\ *(function: CallableType, args_iter: IterableType = [], queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None, features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None)*

    Same as method *run*, but the mount of runnable workers which be created are same as mount of arguments.


**map_with_function**\ *(functions: IterableType[Callable], args_iter: IterableType = [], queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None, features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None)*

    Same as method *run*, but the mount of runnable workers which be created are same as mount of functions.


**close**\ *(workers: Union[_MRTasks, List[_MRTasks]])*

    Close the resource of runnable worker(s).


**result**\ *()*

    Get the return values which be returned by function of runnable workers.

    Will deprecate in version 0.17.0. Change to be a protected function
    and be called in methods *start_new_worker*, *run*, *map* and *map_with_function*.



SimpleExecutor
================

*module* multirunnable.executor

*class*  multirunnable.executor.\ **SimpleExecutor**\ *(executors: int, mode: _RunningMode = None)*


**_initial_running_strategy**\ *()*

    Initial running strategy object which executor uses. The running
    strategy be controlled by option *mode*.



AdapterExecutor
=================

*module* multirunnable.executor

*class*  multirunnable.executor.\ **AdapterExecutor**\ *(strategy: _General_Runnable_Type = None)*


**_initial_running_strategy**\ *()*

    Initial running strategy object which executor uses. It would annotate the global
    variable *General_Runnable_Strategy* with the strategy object it gets from parameter
    *strategy*.

