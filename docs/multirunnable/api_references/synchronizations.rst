==================
Synchronizations
==================

Instantiating and operating features in *multirunnable* is classified to 2 modules.
Modules in subpackage *multirunnable.adapter* be a factories which has responsibility
of generating target instance of running strategy. And for *multirunnable.api*,
its responsibility for operating.

It will have a new feature in version 0.17.0 about integrating factory and operators
into an object to let client site uses it conveniently and clearly.

Adapter Modules
================

*module* multirunnable.adapter

It focuses on generating instance but doesn't care about how to operating it.
It's an adapter to generate the target instance, so it would returns different
instance with different *RunningMode*. Below are the mapping table about which
instance it generates with different *RunningMode*:

+-----------------------+------------------------------+--------------------------------------------+
|         Adapter       |         Running Mode         |               Truly Instance               |
+=======================+==============================+============================================+
|                       |            Parallel          |            multiprocessing.Lock            |
+                       +------------------------------+--------------------------------------------+
|                       |           Concurrent         |                threading.Lock              |
+         Lock          +------------------------------+--------------------------------------------+
|                       |    Coroutine (Green Thread)  |             gevent.threading.Lock          |
+                       +------------------------------+--------------------------------------------+
|                       |    Coroutine (Asynchronous)  |             asyncio.locks.Lock             |
+-----------------------+------------------------------+--------------------------------------------+
|                       |            Parallel          |            multiprocessing.RLock           |
+                       +------------------------------+--------------------------------------------+
|                       |           Concurrent         |               threading.RLock              |
+         RLock         +------------------------------+--------------------------------------------+
|                       |    Coroutine (Green Thread)  |              gevent.lock.RLock             |
+                       +------------------------------+--------------------------------------------+
|                       |    Coroutine (Asynchronous)  |            asyncio.locks.RLock             |
+-----------------------+------------------------------+--------------------------------------------+
|                       |            Parallel          |          multiprocessing.Semaphore         |
+                       +------------------------------+--------------------------------------------+
|                       |           Concurrent         |             threading.Semaphore            |
+        Semaphore      +------------------------------+--------------------------------------------+
|                       |    Coroutine (Green Thread)  |            gevent.lock.Semaphore           |
+                       +------------------------------+--------------------------------------------+
|                       |    Coroutine (Asynchronous)  |           asyncio.locks.Semaphore          |
+-----------------------+------------------------------+--------------------------------------------+
|                       |            Parallel          |     multiprocessing.BoundedSemaphore       |
+                       +------------------------------+--------------------------------------------+
|                       |           Concurrent         |         threading.BoundedSemaphore         |
+   Bounded Semaphore   +------------------------------+--------------------------------------------+
|                       |    Coroutine (Green Thread)  |         gevent.lock.BoundedSemaphore       |
+                       +------------------------------+--------------------------------------------+
|                       |    Coroutine (Asynchronous)  |      asyncio.locks.BoundedSemaphore        |
+-----------------------+------------------------------+--------------------------------------------+
|                       |            Parallel          |           multiprocessing.Event            |
+                       +------------------------------+--------------------------------------------+
|                       |           Concurrent         |              threading.Event               |
+         Event         +------------------------------+--------------------------------------------+
|                       |    Coroutine (Green Thread)  |                gevent.event.Event          |
+                       +------------------------------+--------------------------------------------+
|                       |    Coroutine (Asynchronous)  |                asyncio.Event               |
+-----------------------+------------------------------+--------------------------------------------+
|                       |            Parallel          |          multiprocessing.Condition         |
+                       +------------------------------+--------------------------------------------+
|                       |           Concurrent         |             threading.Condition            |
+       Condition       +------------------------------+--------------------------------------------+
|                       |    Coroutine (Green Thread)  |                (Not Support)               |
+                       +------------------------------+--------------------------------------------+
|                       |    Coroutine (Asynchronous)  |              asyncio.Condition             |
+-----------------------+------------------------------+--------------------------------------------+

Lock Modules
-------------

*module* multirunnable.adapter.lock

The module doesn't only response of *Lock*. All synchronization features which could limit
the performance but DOES NOT communicate with each others like *Lock*, *Semaphore*, etc.

It will be modified to naming as *LockFactory* in version 0.17.0. Same as classes in it (Lock, Semaphore, etc).

Lock
~~~~~~

*class* multirunnable.adapter.lock.\ **Lock**
    The implement about generating *Lock* instance.

**get_instance**\ *(**kwargs)*
    Instantiate the *Lock* instance by FeatureMode which be assigned by RunningMode.

    It could pass arguments if its instantiating needs.

**globalize_instance**\ *(obj)*
    Assign the object as a global variable.

RLock
~~~~~~~

*class* multirunnable.adapter.lock.\ **RLock**
    It's same as *multirunnable.adapter.lock.Lock* but for *RLock*.

Semaphore
~~~~~~~~~~~

*class* multirunnable.adapter.lock.\ **Semaphore**
    It's same as *multirunnable.adapter.lock.Lock* but for *Semaphore*.

Bounded Semaphore
~~~~~~~~~~~~~~~~~~~

*class* multirunnable.adapter.lock.\ **BoundedSemaphore**
    It's same as *multirunnable.adapter.lock.Lock* but for *BoundedSemaphore*.


Communication Modules
----------------------

*module* multirunnable.adapter.communication

All synchronization features which could limit the performance AND could communicate with each others like *Event*, *Condition*.

It will be modified to naming as *CommunicationFactory* in version 0.17.0. Same as classes in it (Event, Condition).

Event
~~~~~~~

*class* multirunnable.adapter.communication.\ **Event**
    It's same as *multirunnable.adapter.lock.Lock* but for *Event*.


Condition
~~~~~~~~~~~

*class* multirunnable.adapter.communication.\ **Condition**
    It's same as *multirunnable.adapter.lock.Lock* but for *Condition*.



API Modules
=============

*module* multirunnable.api

All operators of *MultiRunnable* is the responsibility of this subpackage.
Including synchronizations like *Lock*, *Semaphore* or something like this and retry mechanism.
For synchronization features, *multirunnable.adapter* focus on generating instance, *multirunnable.api* focus on operating something with the instance.

Operator Modules
-----------------

*module* multirunnable.api.operator

This module responses of some operators of synchronization-features.

LockOperator
~~~~~~~~~~~~~~

*class* multirunnable.api.operator.\ **LockOperator**\ *()*
    Operators of feature *Lock*.
    This feature do the same thing as the truly instance we call. Please refer to below to get more details:

    * `Parallel Lock <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Lock>`_
    * `Concurrent Lock <https://docs.python.org/3/library/threading.html#lock-objects>`_
    * `Coroutine - Green Thread Lock <https://www.gevent.org/api/gevent.lock.html>`_
    * `Coroutine - Asynchronous Lock <https://docs.python.org/3/library/asyncio-sync.html#asyncio.Lock>`_

**_get_feature_instance**\ *()*
    Return a *Lock* instance which be get from global variable be saved in module *multirunnable.api.manage*.
    Therefore, this return value would be the same as *multirunnable.api.manage.Running_Lock*.

**acquire**\ *()*
    Acquire a lock to limit performance so that it's force to run ONLY ONE runnable object at the same time.

**release**\ *()*
    Release the lock to let other runnable objects could acquire it.


RLockOperator
~~~~~~~~~~~~~~

*class* multirunnable.api.operator.\ **RLockOperator**\ *()*
    Operators of feature *RLock*.
    This feature do the same thing as the truly instance we call. Please refer to below to get more details:

    * `Parallel RLock <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.RLock>`_
    * `Concurrent RLock <https://docs.python.org/3/library/threading.html#rlock-objects>`_
    * `Coroutine - Green Thread RLock <https://www.gevent.org/api/gevent.lock.html>`_
    * Coroutine - Asynchronous does NOT support this feature

**_get_feature_instance**\ *()*
    Same as *LockOperator._get_feature_instance*. It returns value would be the
    same as *multirunnable.api.manage.Running_RLock*.

**acquire**\ *(blocking: bool = True, timeout: int = -1)*
    Acquire a lock to limit performance so that it's force to run ONLY ONE runnable object at the same time.
    Different is it could acquire lock again and again in runtime. But remember, how many it acquires, how many it needs to release.

**release**\ *()*
    Same as *Lock.acquire*. Difference is program would keep run util last one *release* be called.


SemaphoreOperator
~~~~~~~~~~~~~~~~~~~

*class* multirunnable.api.operator.\ **SemaphoreOperator**\ *()*
    Operators of feature *Semaphore*.
    This feature do the same thing as the truly instance we call. Please refer to below to get more details:

    * `Parallel Semaphore <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Semaphore>`_
    * `Concurrent Semaphore <https://docs.python.org/3/library/threading.html#semaphore-objects>`_
    * `Coroutine - Green Thread Semaphore <https://www.gevent.org/api/gevent.lock.html>`_
    * `Coroutine - Asynchronous Semaphore <https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore>`_

**_get_feature_instance**\ *()*
    Same as *LockOperator._get_feature_instance*. It returns value would be the
    same as *multirunnable.api.manage.Running_Semaphore*.

**acquire**\ *(blocking: bool = True, timeout: int = None)*
    It's mostly same as *Lock*. It force to only one runnable object could run at the same time with *Lock*.
    For *Semaphore*, it permits multiple runnable objects to run simultaneously and the permitted amount
    is the value of option *value* of *multirunnable.adapter.lock.Semaphore*.

**release**\ *(n: int = 1)*
    The logic is same as *Lock.release* but be used for *Semaphore*.


BoundedSemaphoreOperator
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.api.operator.\ **BoundedSemaphoreOperator**\ *()*
    Operators of feature *Bounded Semaphore*.
    This feature do the same thing as the truly instance we call. Please refer to below to get more details:

    * `Parallel Bounded Semaphore <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.BoundedSemaphore>`_
    * `Concurrent Bounded Semaphore <https://docs.python.org/3/library/threading.html#semaphore-objects>`_
    * `Coroutine - Green Thread Bounded Semaphore <https://www.gevent.org/api/gevent.lock.html>`_
    * `Coroutine - Asynchronous Bounded Semaphore <https://docs.python.org/3/library/asyncio-sync.html#asyncio.BoundedSemaphore>`_

**_get_feature_instance**\ *()*
    Same as *LockOperator._get_feature_instance*. It returns value would be the
    same as *multirunnable.api.manage.Running_Bounded_Semaphore*.

**acquire**\ *(blocking: bool = True, timeout: int = None)*
    This implement is same as *SemaphoreOperator.acquire*.

**release**\ *(n: int = 1)*
    It's also same as *SemaphoreOperator.acquire* but the only one different is
    it has limitation (the argument *n*) in every time it releases.


EventOperator
~~~~~~~~~~~~~~~

*class* multirunnable.api.operator.\ **EventOperator**\ *()*
    Operators of feature *Event*.
    This feature do the same thing as the truly instance we call. Please refer to below to get more details:

    * `Parallel Event <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Event>`_
    * `Concurrent Event <https://docs.python.org/3/library/threading.html#event-objects>`_
    * `Coroutine - Green Thread Event <https://www.gevent.org/api/gevent.event.html>`_
    * `Coroutine - Asynchronous Event <https://docs.python.org/3/library/asyncio-sync.html#asyncio.Event>`_

**_event_instance**\ *()*
    Return the *Event* instance.

**_get_feature_instance**\ *()*
    Same as *LockOperator._get_feature_instance*. It returns value would be the
    same as *multirunnable.api.manage.Running_Event*.

**set**\ *()*
    Set a flag to tell other runnable objects could run.

**is_set**\ *()*
    Return bool type value. It's *True* if flag be set or it's *False*.

**wait**\ *(timeout: int = None)*
    Let runnable object waits util flag be set by the method *set*.

**clear**\ *()*
    Clear all flags.


ConditionOperator
~~~~~~~~~~~~~~~~~~~

*class* multirunnable.api.operator.\ **ConditionOperator**\ *()*
    Operators of feature *Condition*.
    This feature do the same thing as the truly instance we call. Please refer to below to get more details:

    * `Parallel Condition <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Condition>`_
    * `Concurrent Condition <https://docs.python.org/3/library/threading.html#condition-objects>`_
    * Coroutine - Green Thread does NOT support this feature
    * `Coroutine - Asynchronous Condition <https://docs.python.org/3/library/asyncio-sync.html#asyncio.Condition>`_

**_get_feature_instance**\ *()*
    Same as *LockOperator._get_feature_instance*. It returns value would be the
    same as *multirunnable.api.manage.Running_Condition*.

**acquire**\ *(blocking: bool = True, timeout: int = None)*
    Acquire a lock to limit performance. It's same as *LockOperator.acquire*.

**release**\ *()*
    Same as *LockOperator.release*.

**wait**\ *(timeout: int = None)*
    Wait util notified or util a timeout occurs.

**wait_for**\ *(predicate, timeout: int = None)*
    Wait until a condition evaluates to true.

**notify**\ *(n: int = 1)*
    By default, wait up one runnable object on this condition.

**notify_all**\ *()*
    Wait up all runnable objects on this condition.

