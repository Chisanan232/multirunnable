=========
Context
=========

It provides APIs to get some detail information of context or one specific worker.
In the *multirunnable* realm, *worker* could be mean *process*, *thread*, *green thread* or *async task* with different strategy.

Below are the mapping table of *worker* with different strategy and Python package:

+-------------------+----------------------+--------------------+
|       Worker      |    Python Package    |       Strategy     |
+===================+======================+====================+
|      Process      |    multiprocessing   |       Parallel     |
+-------------------+----------------------+--------------------+
|       Thread      |       threading      |     Concurrent     |
+-------------------+----------------------+--------------------+
|    Green Thread   |        gevent        |     GreenThread    |
+-------------------+----------------------+--------------------+
|     Async Task    |        asyncio       |    Asynchronous    |
+-------------------+----------------------+--------------------+

Context
========

*module* multirunnable.adapter

This module be an adapter to get the context of mapping worker with *RunningMode* so that it doesn't need to use different object of different sub-package.
It also could get the context via module in each strategy.

This is new in version 0.17.0.

*class* multirunnable.adapter.\ **context**\
    All the functions in the module are *static method*. It focus on context state or information
    like how many activate workers right now or current worker ID, etc.

*staticmethod* **get_current_worker**\ *()*

    Get the instance of current  worker. From above all, it may get *Process*, *Thread*, *Greenlet* or *Task* object.

        Return:
            An object of *Process*, *Thread*, *Greenlet* or *Task*.


*staticmethod* **get_parent_worker**\ *()*

    Get the instance of parent worker means it's the worker which generate and activate current worker.

        Return:
            An object of *Process*, *Thread*, *Greenlet* or *Task*.


*staticmethod* **current_worker_is_parent**\ *()*

    Return *True* if current worker is parent for each workers it activates, or it returns *False*.

        Return:
            A boolean value.


*staticmethod* **get_current_worker_ident**\ *()*

    Get ID of current worker.

        Return:
            A string value.


*staticmethod* **get_current_worker_name**\ *()*

    Get name of current worker.

        Return:
            A string value.


*staticmethod* **current_worker_is_alive**\ *()*

    Return *True* if current worker is activated in running, or it returns *False*.

        Return:
            A boolean value.


*staticmethod* **active_workers_count**\ *()*

    Get the count of all workers it activates.

        Return:
            An integer value.


*staticmethod* **children_workers**\ *()*

    Get a list which saves instances of all worker.

        Return:
            A list of instances of *Process*, *Thread*, *Greenlet* or *Task*.
