==============
Pools Modules
==============

Pool modules means a pool of runnable objects like Process (Parallel),
Thread (Concurrent), Green Thread (Coroutine) or Task (Asynchronous).
It would run as the runnable you set with option *mode* (:doc:`./mode`).


Pool
=======

*module* multirunnable.pool

*class* multirunnable.pool.\ **Pool**
    An abstracted class which implement mostly all methods. The left one abstract
    method *_initial_running_strategy* is generating running strategy with option *mode*.

    About **Pool** object in *MultiRunnable*, it's an adapter which dispatches APIs to use
    APIs of one specific running strategy. It encapsulates about which running strategy you need to instantiate to use.
    Developers only needs to set the *RunningMode* to let it instantiates target running strategy by itself,
    so developers could focus on the usages of *Pool* but doesn't care about running strategy instantiating.

    Therefore, all the APIs is the same as *PoolRunnableStrategy*.

    About️ option *mode* and *executors*, it will be deprecated in version 0.17.0.


SimplePool
============

*module* multirunnable.pool

*class* multirunnable.pool.\ **SimplePool**

**_initial_running_strategy**
    Initial running strategy object which executor uses. The running
    strategy be controlled by option *mode*.

