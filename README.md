# MultiRunnable

[![Supported Versions](https://img.shields.io/pypi/pyversions/multirunnable.svg?logo=python&logoColor=FBE072)](https://pypi.org/project/multirunnable)
[![Release](https://img.shields.io/github/release/Chisanan232/multirunnable.svg?label=Release)](https://github.com/Chisanan232/multirunnable/releases)
[![PyPI version](https://badge.fury.io/py/MultiRunnable.svg)](https://badge.fury.io/py/MultiRunnable)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6733a68742a64b3dbcfa57b1309de4ce)](https://www.codacy.com/gh/Chisanan232/multirunnable/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Chisanan232/multirunnable&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/multirunnable/badge/?version=latest)](https://multirunnable.readthedocs.io/en/latest/?badge=latest)

| OS | Building Status | Coverage Status |
|------------|------------|--------|
| Linux |[![CircleCI](https://circleci.com/gh/Chisanan232/multirunnable.svg?style=svg)](https://app.circleci.com/pipelines/github/Chisanan232/multirunnable)|[![codecov](https://codecov.io/gh/Chisanan232/multirunnable/branch/master/graph/badge.svg?token=E2AGK1ZIDH)](https://codecov.io/gh/Chisanan232/multirunnable)|
| Linux |[![multirunnable testing](https://github.com/Chisanan232/multirunnable/actions/workflows/ci.yml/badge.svg)](https://github.com/Chisanan232/multirunnable/actions/workflows/ci.yml)|[![codecov](https://codecov.io/gh/Chisanan232/multirunnable/branch/master/graph/badge.svg?token=E2AGK1ZIDH)](https://codecov.io/gh/Chisanan232/multirunnable)|
| Windows |[![Build status](https://ci.appveyor.com/api/projects/status/v0nq38jtof6vcm23?svg=true)](https://ci.appveyor.com/project/Chisanan232/multirunnable)|[![Coverage Status](https://coveralls.io/repos/github/Chisanan232/multirunnable/badge.svg?branch=master)](https://coveralls.io/github/Chisanan232/multirunnable?branch=master)|

A Python library integrates the APIs of 3 strategies (Parallel, Concurrent, Coroutine) and 4 libraries (multiprocessing, threading, gevent, asyncio) to help developers build parallelism humanly.

[Overview](#overview) | [Quickly Start](#quickly-start) | [Syntactic Sugar](#syntactic-sugar) | [Resource](#resource) | [Code Example](https://github.com/Chisanan232/multirunnable/tree/master/example)
<hr>

## Overview

Package '_multirunnable_' is a library which could easily build a parallelism with different running strategy by mode option. 
Currently, it has 4 options could use: Parallel, Concurrent, GreenThread and Asynchronous.

Here's an example which implements parallelism as concurrent with _multirunnable_:

```python
from multirunnable import SimpleExecutor, RunningMode
import time

Workers_Number = 5

def function(index):
    print(f"This is function with index {index}")
    time.sleep(3)


if __name__ == '__main__':
  
    executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=Workers_Number)
    executor.run(function=function, args={"index": f"test_arg"})
```

How about parallel? Only one thing you need to do: change the mode.

```python
... # Any code is the same

executor = SimpleExecutor(mode=RunningMode.Parallel, executors=Workers_Number)

... # Any code is the same
```

Program would turn to run as parallel and work finely. <br>
Want change to use other way to run? Change the Running Mode, that's all. <br>

> ⚠️ **Parallel, Concurrent and GreenThread are in common but Asynchronous isn't.** <br>
From above all, we could change the mode to run the code as the running strategy we configure. 
However, it only accepts 'awaitable' function to run as asynchronous in Python. 
In the other word, you must remember add keyword 'async' before function which is the target to run with _multirunnable_.


## Quickly Start

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


## Syntactic Sugar

It could implement some features via Python decorator in _MultiRunnable_.

For example, Lock via decorator **RunWith** (it's **AsyncRunWith** with Asynchronous):

```python
from multirunnable.api import RunWith
import time

@RunWith.Lock
def lock_function():
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
```

✨👀 **All below features support decorator:** <br>
*Lock*, *RLock*, *Semaphore*, *Bounded Semaphore*.


## Resource

The [documentation](https://multirunnable.readthedocs.io) contains more details, and examples.

