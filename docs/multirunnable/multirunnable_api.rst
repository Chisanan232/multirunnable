MultiRunnable API reference
=================================


1 Mode Objects
~~~~~~~~~~~~~~~~~~~~

*module* multirunnable.mode

1.1 RunningMode
-----------------

*class* multirunnable.mode.\ **RunningMode**

RunningMode.\ **Parallel**

RunningMode.\ **Concurrent**

RunningMode.\ **GreenThread**

RunningMode.\ **Asynchronous**



1.2 FeatureMode
----------------

*class* multirunnable.mode.\ **FeatureMode**

FeatureMode.\ **Parallel**

FeatureMode.\ **Concurrent**

FeatureMode.\ **GreenThread**

FeatureMode.\ **Asynchronous**



2 Executor Objects
~~~~~~~~~~~~~~~~~~~~

*module* multirunnable.executor

*class* multirunnable.executor.\ **Executor**

Executor.\ **start_new_worker**

Executor.\ **run**

Executor.\ **map**

Executor.\ **map_with_function**

Executor.\ **terminal**

Executor.\ **kill**

Executor.\ **result**


*class* multirunnable.executor.\ **SimpleExecutor**



3 Pool Objects
~~~~~~~~~~~~~~~~~~~~

*module* multirunnable.pool

*class* multirunnable.pool.\ **Pool**

Pool.\ **initial**

Pool.\ **apply**

Pool.\ **async_apply**

Pool.\ **map**

Pool.\ **async_map**

Pool.\ **map_by_args**

Pool.\ **async_map_by_args**

Pool.\ **imap**

Pool.\ **imap_unordered**

Pool.\ **close**

Pool.\ **terminal**

Pool.\ **get_result**


*class* multirunnable.pool.\ **SimplePool**



4 Adapter Objects
~~~~~~~~~~~~~~~~~~~~

*module* multirunnable.adapter

4.1 Lock Module
----------------------------

*module* multirunnable.adapter.lock

4.1.1 Lock
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.adapter.lock.\ **Lock**

Lock.\ **get_instance**

Lock.\ **globalize_instance**

4.1.2 RLock
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.adapter.lock.\ **RLock**

RLock.\ **get_instance**

RLock.\ **globalize_instance**

4.1.3 Semaphore
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.adapter.lock.\ **Semaphore**

Semaphore.\ **get_instance**

Semaphore.\ **globalize_instance**

4.1.4 Bounded Semaphore
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.adapter.lock.\ **BoundedSemaphore**

BoundedSemaphore.\ **get_instance**

BoundedSemaphore.\ **globalize_instance**



4.2 Communication Module
----------------------------

*module* multirunnable.adapter.communication


4.2.1 Event
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.adapter.communication.\ **Event**

Event.\ **get_instance**

Event.\ **globalize_instance**


4.2.2. Condition
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.adapter.communication.\ **Condition**

Condition.\ **get_instance**

Condition.\ **globalize_instance**



5 API Objects
~~~~~~~~~~~~~~~~~~~~

*module* multirunnable.api

5.1 Operator Module
----------------------------

*module* multirunnable.api.operator

5.1.1 LockOperator
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.api.operator.\ **LockOperator**

LockOperator.\ **get_instance**

LockOperator.\ **globalize_instance**


5.2 Decorator Module
----------------------------

*module* multirunnable.api.decorator

5.2.1 retry
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.api.decorator.\ **LockOperator**

LockOperator.\ **get_instance**

LockOperator.\ **globalize_instance**


5.3 Manage Module
----------------------------

*module* multirunnable.api.manage

5.3.1 LockOperator
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.api.operator.\ **LockOperator**

LockOperator.\ **get_instance**

LockOperator.\ **globalize_instance**



6 Strategy Objects
~~~~~~~~~~~~~~~~~~~~

6.1 Parallel Module
----------------------------

*module* multirunnable.parallel

6.1.1 Process Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.parallel.strategy.\ **ProcessStrategy**

ProcessStrategy.\ **get_instance**

ProcessStrategy.\ **globalize_instance**


6.1.2 Process Pool Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.parallel.strategy.\ **ProcessPoolStrategy**

ProcessPoolStrategy.\ **get_instance**

ProcessPoolStrategy.\ **globalize_instance**



6.2 Concurrent Module
----------------------------

*module* multirunnable.concurrent

6.2.1 Thread Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.concurrent.strategy.\ **ThreadStrategy**

ThreadStrategy.\ **get_instance**

ThreadStrategy.\ **globalize_instance**

6.2.2 Thread Pool Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.concurrent.strategy.\ **ThreadPoolStrategy**

ThreadPoolStrategy.\ **get_instance**

ThreadPoolStrategy.\ **globalize_instance**



6.3 Coroutine Module
----------------------------

*module* multirunnable.coroutine

6.3.1 Coroutine Strategy -- Green Thread Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.coroutine.strategy.\ **GreenThreadStrategy**

GreenThreadStrategy.\ **get_instance**

GreenThreadStrategy.\ **globalize_instance**


6.3.2 Coroutine Strategy -- Green Thread Pool Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.coroutine.strategy.\ **GreenThreadPoolStrategy**

GreenThreadPoolStrategy.\ **get_instance**

GreenThreadPoolStrategy.\ **globalize_instance**


6.3.3 Coroutine Strategy -- Asynchronous Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.coroutine.strategy.\ **AsynchronousStrategy**

AsynchronousStrategy.\ **get_instance**

AsynchronousStrategy.\ **globalize_instance**



7 Persistence Objects
~~~~~~~~~~~~~~~~~~~~

7.1 Database Modules
----------------------------

*module* multirunnable.persistence.database

7.1.1 Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.parallel.strategy.\ **ProcessStrategy**

ProcessStrategy.\ **get_instance**

ProcessStrategy.\ **globalize_instance**


7.2 File Modules
----------------------------

*module* multirunnable.persistence.database

7.2.1 Files
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.parallel.strategy.\ **ProcessStrategy**

ProcessStrategy.\ **get_instance**

ProcessStrategy.\ **globalize_instance**



