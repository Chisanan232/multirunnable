==============
Mode Objects
==============

*module* multirunnable.mode

*multirunnable* is a Python package which could run as different way (Parallel, Concurrent, Coroutine) with different strategy.
The key option to control which way to run is *RunningMode*. Option *FeatureMode* be used for features like Lock, Semaphore, Condition, etc.

RunningMode
=============

*Enumeration* multirunnable.mode.\ **RunningMode**

RunningMode.\ **Parallel**
    Control *multirunnable* should be run as parallelism with Parallel.
    It would dispatch to use module *multirunnable.parallel.strategy*.
    The objects it would use is *ProcessStrategy* or *ProcessPoolStrategy*.

RunningMode.\ **Concurrent**
    Control *multirunnable* should be run as parallelism with Concurrent.
    It would dispatch to use module *multirunnable.concurrent.strategy*.
    The objects it would use is *ThreadStrategy* or *ThreadPoolStrategy*.

RunningMode.\ **GreenThread**
    Control *multirunnable* should be run as parallelism with Green Thread.
    It would dispatch to use module *multirunnable.coroutine.strategy*.
    The objects it would use is *GreenThreadStrategy* or *GreenThreadPoolStrategy*.

RunningMode.\ **Asynchronous**
    Control *multirunnable* should be run as parallelism with Asynchronous.
    It would dispatch to use module *multirunnable.coroutine.strategy*.
    The objects it would use is *AsynchronousStrategy*.



FeatureMode
=============

*Enumeration* multirunnable.mode.\ **FeatureMode**

FeatureMode.\ **Parallel**
    Control *multirunnable* instantiates feature (Lock, Semaphore, etc) instance for Parallel.
    It would dispatch to use module *multirunnable.parallel.features*.
    The objects it would use is *ProcessLock* or *ProcessCommunication*.

FeatureMode.\ **Concurrent**
    Control *multirunnable* instantiates feature (Lock, Semaphore, etc) instance for Concurrent.
    It would dispatch to use module *multirunnable.concurrent.features*.
    The objects it would use is *ThreadLock* or *ThreadCommunication*.

FeatureMode.\ **GreenThread**
    Control *multirunnable* instantiates feature (Lock, Semaphore, etc) instance for Green Thread.
    It would dispatch to use module *multirunnable.coroutine.features*.
    The objects it would use is *GreenThreadLock* or *GreenThreadCommunication*.

FeatureMode.\ **Asynchronous**
    Control *multirunnable* instantiates feature (Lock, Semaphore, etc) instance for Asynchronous.
    It would dispatch to use module *multirunnable.coroutine.features*.
    The objects it would use is *AsynchronousLock* or *AsynchronousCommunication*.

