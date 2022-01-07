=========================
MultiRunnable Decorator
=========================


*module* multirunnable.api.decorator

retry
-------

It's possible that occurs unexpected something when running. Sometimes, it needs
to catch that exceptions or errors to do some handling, it even needs to do something
finally and keep going run the code. That's the reason this feature exists.

*decorator* multirunnable.api.decorator.\ **retry**\ *(timeout)*
    Decorate on target function which needs to implement its customized retry handling.

*decorator* **retry.initialization**\ *(*args, **kwargs)*
    The function which should be run first before run target function.
    Default implementation is doing nothing.
    The usage is decorating as target function annotation name and call **.initialization** method:

*decorator* **retry.done_handling**\ *(func_result)*
    It will return value after run completely target function. This feature argument
    receives the result. You could do some result-handling here to reach your own target,
    and it will return it out.
    Default implementation is doing nothing, just return the result it gets.
    The usage is decorating as target function annotation name and call **.done_handling** method.

*decorator* **retry.error_handling**\ *(e)*
    Target to handle every exception or error. So the function argument absolutely receives exception or error.
    Default implementation is raising any exception or error it gets.
    The usage is decorating as target function annotation name and call **.error_handling** method.

*decorator* **retry.final_handling**\ *(func_result)*
    It's the feature run something which MUST to do. For example, close IO.
    Default implementation is doing nothing.
    The usage is decorating as target function annotation name and call **.final_handling** method.


Example usage of decorator *retry*:

.. code-block:: python

    from multirunnable.api import retry

    @retry(timeout=3)
    def fail_function(*args, **kwargs):
        raise Exception("Test for error")

    @fail_function.initialization
    def initial():
        ... # Do something before run target function

    @fail_function.done_handling
    def done(result):
        ... # Do something after done target function

    @fail_function.error_handling
    def error(error):
        ... # Do something to handle the error if it catch any exception.

    @fail_function.final_handling
    def final():
        ... # No matter what things happen, it must to do something finally.


async_retry
-------------

*decorator* multirunnable.api.decorator.\ **async_retry**\ *(timeout)*
    Asynchronous version of decorator *async_retry*. All usages of APIs are same as it, too.


RunWith
----------

*decorator* multirunnable.api.decorator.\ **RunWith**
    This is a syntactic sugar for features (Lock, Semaphore, etc) of *multirunnable*.
    Please refer to the :doc:`./synchronizations` to get more details.

*decorator* RunWith.**Lock**\ *(function)*
    Using Lock feature via Python decorator with object *RunWith*.

*decorator* RunWith.**RLock**\ *(function)*
    Using RLock feature via Python decorator with object *RunWith*.

*decorator* RunWith.**Semaphore**\ *(function)*
    Using Semaphore feature via Python decorator with object *RunWith*.

*decorator* RunWith.**BoundedSemaphore**\ *(function)*
    Using BoundedSemaphore feature via Python decorator with object *RunWith*.


Example usage of decorator *RunWith*:

.. code-block:: python

    from multirunnable.api import RunWith
    import time

    @RunWith.Lock
    def lock_function():
        print("Running process in lock and will sleep 2 seconds.")
        time.sleep(2)
        print(f"Wake up process and release lock.")


AsyncRunWith
-------------

*decorator* multirunnable.api.decorator.\ **AsyncRunWith**
    Asynchronous version of decorator *RunWith*. All usages of APIs are same as it, too.

