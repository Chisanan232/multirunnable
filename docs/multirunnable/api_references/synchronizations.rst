==================
Synchronizations
==================

Instantiating and operating features in *multirunnable* is classified to 2 modules.
Modules in subpackage *multirunnable.adapter* be a factories which has responsibility
of generating target instance of running strategy. And for *multirunnable.api*,
its responsibility for operating.

It will have a new feature in version 0.17.0 about integrating factory and operators
into an object to let client site uses it conveniently and clearly.

Factory Modules
================

*module* multirunnable.factory

It focuses on generating instance but doesn't care about how to operating it.
It's an factory to generate the target instance, so it would returns different
instance with different *RunningMode*. Below are the mapping table about which
instance it generates with different *RunningMode*:

+-----------------------+------------------------------+--------------------------------------------+
|         Factory       |         Running Mode         |               Truly Instance               |
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

*module* multirunnable.factory.lock

The module doesn't only response of *Lock*. All synchronization features which could limit
the performance but DOES NOT communicate with each others like *Lock*, *Semaphore*, etc.

It was named as *LockAdapter* before version 0.17.0. Same as classes in it (Lock, Semaphore, etc).

.. _Factory.Lock - LockFactory:

LockFactory
~~~~~~~~~~~~~

*class* multirunnable.factory.lock.\ **LockFactory**
    The implement about generating *Lock* instance.

**get_instance**\ *(**kwargs)*
    Instantiate the *Lock* instance by FeatureMode which be assigned by RunningMode.

    It could pass arguments if its instantiating needs.

**globalize_instance**\ *(obj)*
    Assign the object as a global variable.

.. _Factory.Lock - RLockFactory:

RLockFactory
~~~~~~~~~~~~~~

*class* multirunnable.factory.lock.\ **RLockFactoryFactory**
    It's same as *multirunnable.factory.lock.LockFactory* but for *RLock*.

.. _Factory.Lock - SemaphoreFactory:

SemaphoreFactory
~~~~~~~~~~~~~~~~~~

*class* multirunnable.factory.lock.\ **SemaphoreFactoryFactory**
    It's same as *multirunnable.factory.lock.LockFactory* but for *Semaphore*.

.. _Factory.Lock - BoundedSemaphoreFactory:

BoundedSemaphoreFactory
~~~~~~~~~~~~~~~~~~~~~~~~~~

*class* multirunnable.factory.lock.\ **BoundedSemaphoreFactory**
    It's same as *multirunnable.factory.lock.LockFactory* but for *BoundedSemaphore*.


Communication Modules
----------------------

*module* multirunnable.factory.communication

All synchronization features which could limit the performance AND could communicate with each others like *Event*, *Condition*.

It will be modified to naming as *CommunicationFactory* in version 0.17.0. Same as classes in it (Event, Condition).

.. _Factory.Communication - EventFactory:

EventFactory
~~~~~~~~~~~~~

*class* multirunnable.factory.communication.\ **EventFactory**
    It's same as *multirunnable.factory.lock.LockFactory* but for *Event*.


.. _Factory.Communication - ConditionFactory:

ConditionFactory
~~~~~~~~~~~~~~~~~

*class* multirunnable.factory.communication.\ **ConditionFactory**
    It's same as *multirunnable.factory.lock.LockFactory* but for *Condition*.



API Modules
=============

*module* multirunnable.api

All operators of *MultiRunnable* is the responsibility of this subpackage.
Including synchronizations like *Lock*, *Semaphore* or something like this and retry mechanism.
For synchronization features, *multirunnable.factory* focus on generating instance, *multirunnable.api* focus on operating something with the instance.

Operator Modules
-----------------

*module* multirunnable.api.operator

This module responses of some operators of synchronization-features.

.. _API.Operator - LockOperator:

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


.. _API.Operator - RLockOperator:

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


.. _API.Operator - SemaphoreOperator:

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
    is the value of option *value* of *multirunnable.factory.lock.Semaphore*.

**release**\ *(n: int = 1)*
    The logic is same as *Lock.release* but be used for *Semaphore*.


.. _API.Operator - BoundedSemaphoreOperator:

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


.. _API.Operator - EventOperator:

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


.. _API.Operator - ConditionOperator:

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



Adapter Modules
================

*module* multirunnable.adapter

Subpackage *Adapter* for clear and convenient in usage. It combines the features of both 2 subpackages *Factory* and *API*.

About synchronization usage in *multirunnable*, it divides to 2 sections: *Factory* and *API*.
The former generates instance with *RunningMode*; the latter provides all operators of the instance.
However, it doesn't be clear or be convenient to use sometimes. It also needs to care 2 different objects
when you're using.

Let's demonstrate some different usage between *Adapter* and *Factory* with *API*:

Usage with *Adapter*:

.. code-block:: python

    from multirunnable import RunningMode, SimpleExecutor, sleep
    from multirunnable.adapter import Lock

    _lock = Lock(mode=RunningMode.Parallel, init=True)    # Use Lock feature with Adapter object

    def lock_function():
        _lock.acquire()
        print("This is ExampleTargetFunction.target_function.")
        sleep(3)
        _lock.release()

    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=5)
    executor.run(function=lock_function)


Usage with *Factory* and *API*:

.. code-block:: python

    from multirunnable import RunningMode, SimpleExecutor, sleep
    from multirunnable.api import LockOperator
    from multirunnable.factory import LockFactory

    def lock_function():
        _lock_opt = LockOperator()    # Use Lock feature with Operator object
        _lock_opt.acquire()
        print("This is ExampleTargetFunction.target_function.")
        sleep(3)
        _lock_opt.release()

    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=5)
    lock = LockFactory()    # Use Lock feature with Factory object
    executor.run(function=lock_function, features=lock)


About second one of above demonstrations, it generates instance by object *LockFactory*
and operates the Lock feature with object *LockOperator*. It must to care about what thing
to do and when to call it. But it doesn't if it uses with object *Lock*.

Objects in it has all the attributes of *Factory* and *API*. And the attribute's name
also the same between them. So what attributes *Factory* or *API* they have, what
attributes *Adapter* it has.

The modules of subpackage *Adapter*:

* module: *multirunnable.adapter.lock*

    * Lock
        * :ref:`Factory.Lock - LockFactory`
        * :ref:`API.Operator - LockOperator`
    * RLock
        * :ref:`Factory.Lock - RLockFactory`
        * :ref:`API.Operator - RLockOperator`
    * Semaphore
        * :ref:`Factory.Lock - SemaphoreFactory`
        * :ref:`API.Operator - SemaphoreOperator`
    * BoundedSemaphore
        * :ref:`Factory.Lock - BoundedSemaphoreFactory`
        * :ref:`API.Operator - BoundedSemaphoreOperator`

* module: *multirunnable.adapter.communication*
    * Event
        * :ref:`Factory.Communication - EventFactory`
        * :ref:`API.Operator - EventOperator`
    * Condition
        * :ref:`Factory.Communication - ConditionFactory`
        * :ref:`API.Operator - ConditionOperator`

