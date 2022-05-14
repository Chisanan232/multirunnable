===================
Executors Modules
===================

Executor modules means a unit worker of runnable like Process (Parallel), Thread (Concurrent), Green Thread (Coroutine) or Task (Asynchronous).
It would run as the runnable you set with option *mode* (:doc:`./mode`).


Executor
===========

*module* multirunnable.executor

*class*  multirunnable.executor.\ **Executor**\ *(mode=None, executors=1)*

    An abstracted class which implement mostly all methods. The left one abstract
    method *_initial_running_strategy* is generating running strategy with option *mode*.

    About️ option *mode* and *executors*, it will be deprecated in version 0.17.0.


**start_new_worker**\ *(target, *args, **kwargs)*

    It would initial a runnable worker and run it immediately. It won't close runnable worker.


**run**\ *(function, args, queue_tasks, features)*

    It would do initialing first (before instantiate runnable worker).
    It instantiates runnable workers as the mount by option *executors* and runs them.
    It would close the runnable worker finally.


**map**\ *(function, args_iter, queue_tasks, features)*

    Same as method *run*, but the mount of runnable workers which be created are same as mount of arguments.


**map_with_function**\ *(functions, args_iter, queue_tasks, features)*

    Same as method *run*, but the mount of runnable workers which be created are same as mount of functions.


**terminal**\ *()*

    Terminate runnable worker(s).


**kill**\ *()*

    this function content ...


**result**\ *()*

    Get the return values which be returned by function of runnable workers.

    Will deprecate in version 0.17.0. Change to be a protected function
    and be called in methods *start_new_worker*, *run*, *map* and *map_with_function*.



SimpleExecutor
================

*module* multirunnable.executor

*class*  multirunnable.executor.\ **SimpleExecutor**\ *(mode=None, executors=1)*


**_initial_running_strategy**\ *()*

    Initial running strategy object which executor uses. The running
    strategy be controlled by option *mode*.

