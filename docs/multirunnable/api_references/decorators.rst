=========================
MultiRunnable Decorator
=========================


*module* multirunnable.api.decorator

retry
-------

It's possible that occurs unexpected something when running. Sometimes, it needs
to catch that exceptions or errors to do some handling, it even needs to do something
finally and keep going run the code. That's the reason this feature exists.

*object* multirunnable.api.decorator.\ **retry**

    Decorate on target function which needs to implement its customized retry handling.
    However, it needs to use the different decorators for the different type of function.

    * general function -> multirunnable.api.decorator.\ **retry.function**\ *(timeout: int = 1)*
    * bounded function -> multirunnable.api.decorator.\ **retry.bounded_function**\ *(timeout: int = 1)*

    Actually, it's a **static factory**. It means that you cannot instantiate this object,
    or you will get an RuntimeError. Except for decorator type, all the APIs usage are
    the same between them.

    Still doesn't understand its usage? Don't worry, following demonstration for you:

    * **General function**: multirunnable.api.decorator.\ **retry.function**\ *(timeout: int = 1)*

    .. code-block:: python

        from multirunnable.api import retry

        @retry.function    # Default timeout is 1.
        # @retry.function(timeout=3)    # It also could set the timeout setting.
        def retry_function(*args, **kwargs):
            pass


    * **Bounded function**: multirunnable.api.decorator.\ **retry.bounded_function**\ *(timeout: int = 1)*

    .. code-block:: python

        from multirunnable.api import retry

        class RetryTest:

            @retry.bounded_function    # Default timeout is 1.
            # @retry.bounded_function(timeout=3)    # It also could set the timeout setting.
            def retry_bounded_function(self, *args, **kwargs):
                pass


*decorator* **initialization**\ *(*args, **kwargs)*

    The function which should be run first before run target function.
    Default implementation is doing nothing.
    The usage is decorating as target function annotation name and call **.initialization** method:


*decorator* **done_handling**\ *(func_result)*

    It will return value after run completely target function. This feature argument
    receives the result. You could do some result-handling here to reach your own target,
    and it will return it out.
    Default implementation is doing nothing, just return the result it gets.
    The usage is decorating as target function annotation name and call **.done_handling** method.


*decorator* **error_handling**\ *(e: Exception)*

    Target to handle every exception or error. So the function argument absolutely receives exception or error.
    Default implementation is raising any exception or error it gets.
    The usage is decorating as target function annotation name and call **.error_handling** method.


*decorator* **final_handling**\ *()*

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

*object* multirunnable.api.decorator.\ **async_retry**\ *(timeout)*

    Asynchronous version of decorator *async_retry*. All usages of APIs are same as it, too.


RunWith
----------

*object* multirunnable.api.decorator.\ **RunWith**

    This is a syntactic sugar for features (Lock, Semaphore, etc) of *multirunnable*.
    Please refer to the :doc:`./synchronizations` to get more details.

    By the way, this object also a static factory so that it also cannot be instantiated.


*decorator* **Lock**\ *(*args, **kwargs)*

    Using Lock feature via Python decorator with object *RunWith*.


*decorator* **RLock**\ *(*args, **kwargs)*

    Using RLock feature via Python decorator with object *RunWith*.


*decorator* **Semaphore**\ *(*args, **kwargs)*

    Using Semaphore feature via Python decorator with object *RunWith*.


*decorator* **BoundedSemaphore**\ *(*args, **kwargs)*

    Using BoundedSemaphore feature via Python decorator with object *RunWith*.


Example usage of decorator *RunWith*:

.. code-block:: python

    from multirunnable.api import RunWith

    @RunWith.Lock
    def lock_function():
        pass


AsyncRunWith
-------------

*object* multirunnable.api.decorator.\ **AsyncRunWith**

    Asynchronous version of decorator *RunWith*. All usages of APIs are same as it, too.

