=======================
Quickly Start
=======================

Install this package by pip:

    pip install multirunnable

Write a simple code to run it.

    >>> from multirunnable import SimpleExecutor, RunningMode
    >>> executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
    >>> def function(index):
    ...     print(f"This is function with index {index}")
    ...
    >>> executor.run(function=function, args={"index": f"test_param"})
    This is function with index test_param
    This is function with index test_param
    This is function with index test_param
    >>>

