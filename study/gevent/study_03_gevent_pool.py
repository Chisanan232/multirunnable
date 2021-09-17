from gevent.pool import Pool
from gevent.threadpool import ThreadPool, ThreadPoolExecutor, Greenlet
# from gevent.thread import Greenlet
from gevent.threading import Thread
from gevent import sleep as gthread_sleep
from typing import List
import functools
import itertools
import random
import os



class TestGeventPool:

    __Greenlet_List: List[Greenlet] = []

    @classmethod
    def run_with_spawn(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        for greenlet_index in range(__greenlet_number):
            params = {"index": greenlet_index}
            result = pool.spawn(cls.main_run_fun, **params)
            cls.__Greenlet_List.append(result)

        # for one_gthread in cls.__Greenlet_List:
        #     one_gthread.start()

        gthread_result = []
        for one_gthread in cls.__Greenlet_List:
            one_gthread.join()
            one_gthread_parent = one_gthread.parent
            one_gthread_error = one_gthread.error
            one_gthread_name = one_gthread.name
            one_gthread_ready = one_gthread.ready()
            one_gthread_successful = one_gthread.successful()
            one_gthread_start = one_gthread.started
            one_gthread_loop = one_gthread.loop
            one_gthread_exception = one_gthread.exception
            one_gthread_val = one_gthread.value

            print("+++++++++++++++++++++++++++")
            print("parent: ", one_gthread_parent)
            print("error: ", one_gthread_error)
            print("name: ", one_gthread_name)
            print("ready: ", one_gthread_ready)
            print("successful: ", one_gthread_successful)
            print("started: ", one_gthread_start)
            print("loop: ", one_gthread_loop)
            print("exception: ", one_gthread_exception)
            print("value: ", one_gthread_val)

            gthread_result.append(one_gthread_val)

        print("result: ", gthread_result)



    @classmethod
    def run_with_apply(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        for greenlet_index in range(__greenlet_number):
            params = {"index": greenlet_index}
            result = pool.apply(func=cls.main_run_fun, kwds=params)
            cls.__Greenlet_List.append(result)

        print("result: ", cls.__Greenlet_List)


    @classmethod
    def run_with_apply_async(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        for greenlet_index in range(__greenlet_number):
            params = {"index": greenlet_index}
            result = pool.apply_async(func=cls.main_run_fun, kwds=params)
            cls.__Greenlet_List.append(result)

        for greenlet in cls.__Greenlet_List:
            greenlet.start()    # Can work
            # greenlet.run()      # Can work
            # greenlet.get()      # Can work
            # greenlet.switch()     # Cannot work
            successful = greenlet.successful()
            exc_info = greenlet.exc_info
            value = greenlet.value
            current = greenlet.getcurrent()
            print("current: ", current)
            print("exc_info: ", exc_info)
            print("successful: ", successful)
            print("value: ", value)

        for greenlet in cls.__Greenlet_List:
            greenlet.join()
            dead = greenlet.dead
            print("dead: ", dead)


    @classmethod
    def run_with_apply_cb(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        for _ in range(5):
            result = pool.apply_cb(func=cls.main_run_fun, args=("index_1",), callback=cls.main_run_fun_with_cb)
            cls.__Greenlet_List.append(result)

        print("result: ", cls.__Greenlet_List)


    @classmethod
    def run_with_map(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        result = pool.map(func=cls.main_run_fun, iterable=("index_1", "index_2", "index_3", "index_4", "index_5", "index_6"))
        print("result: ", result)


    @classmethod
    def run_with_map_multiargs(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        params = ("index_1", "index_2", "index_3", "index_4", "index_5", "index_6")
        _params = params[:-1]
        print("_params: ", _params)
        _last_params = params[-1:] * len(_params)
        print("_last_params: ", _last_params)
        _partial_params = functools.partial(cls.main_run_fun_with_args, *_params)
        print("_partial_params: ", _partial_params)
        result = pool.map(func=_partial_params, iterable=_last_params)
        print("result: ", result)


    @classmethod
    def run_with_map_multiargs_2(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        params = [("index_1", "index_2"), ("index_3", "index_4"), ("index_5", "index_6")]
        params_t = [("index_1", "index_2"), ("index_1", "index_4"), ("index_1", "index_2")]
        params_t_set = set(params_t)
        print("params_t: ", params_t)
        print("params_t_set: ", params_t_set)
        # _params = params[:-1]
        # print("_params: ", _params)
        # _last_params = params[-1:] * len(_params)
        # print("_last_params: ", _last_params)
        # _partial_params = functools.partial(cls.main_run_fun_with_args, *_params)
        # print("_partial_params: ", _partial_params)
        result = pool.map(func=cls.main_run_fun_with_args, iterable=params)
        pool.map(cls.main_run_fun_with_args, params, params)
        print("result: ", result)


    @classmethod
    def run_with_map_async(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        __gtheads = pool.map_async(func=cls.main_run_fun, iterable=("index_1", "index_2", "index_3", "index_4", "index_5", "index_6"))
        __gthead_get = __gtheads.get()
        __ready = __gtheads.ready()
        __name = __gtheads.name
        __parent = __gtheads.parent
        __successful = __gtheads.successful()
        __error = __gtheads.error

        __gthread_loop = __gtheads.loop
        __gthread_started = __gtheads.started
        __gthread_val = __gtheads.value
        __exception = __gtheads.exception

        print("__gthead_get: ", __gthead_get)
        print("__ready: ", __ready)
        print("__name: ", __name)
        print("__parent: ", __parent)
        print("__successful: ", __successful)
        print("__error: ", __error)
        print("__gthread_loop: ", __gthread_loop)
        print("__gthread_started: ", __gthread_started)
        print("__gthread_val: ", __gthread_val)
        print("__exception: ", __exception)


    @classmethod
    def run_with_map_cb(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        result = pool.map_cb(func=cls.main_run_fun, iterable=("index_1", "index_2", "index_3", "index_4", "index_5", "index_6"), callback=cls.main_run_fun_with_cb)
        print("result: ", result)


    @classmethod
    def run_with_imap(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        # result = pool.imap(cls.main_run_fun, ("index_1", "index_2", "index_3", "index_4", "index_5", "index_6"))
        # result = pool.imap(cls.main_run_fun, (("index_1", "index_2"), ("index_3", "index_4"), ("index_5", "index_6")))
        result = pool.imap(cls.main_run_fun_with_args, (("index_1", "index_2"), ("index_3", "index_4"), ("index_5", "index_6")))
        result_list = [r for r in result]
        print("result: ", result_list)


    @classmethod
    def run_with_imap_unordered(cls):
        __greenlet_number = 5
        pool = Pool(size=__greenlet_number)
        result = pool.imap_unordered(cls.main_run_fun, ("index_1", "index_2", "index_3", "index_4", "index_5", "index_6"))
        result_list = [r for r in result]
        print("result: ", result_list)


    @classmethod
    def main_run_fun(cls, index):
        print(f"Run the function with Greenlet! - {index}, pid: {os.getpid()}")
        __random_sleep = random.randrange(1, 10)
        print(f"Will sleep for {__random_sleep} seconds.")
        gthread_sleep(__random_sleep)
        return "Yee"


    @classmethod
    def main_run_fun_with_args(cls, *args, **kwargs):
        print(f"Run the function(*args) with Greenlet! - {args}, pid: {os.getpid()}")
        print(f"Run the function(**kwargs) with Greenlet! - {kwargs}, pid: {os.getpid()}")
        __random_sleep = random.randrange(1, 10)
        print(f"Will sleep for {__random_sleep} seconds.")
        gthread_sleep(__random_sleep)
        return "Yee"


    @classmethod
    def main_run_fun_with_cb(self, *args, **kwargs):
        print("This is testing callback function.")
        print("Callback function args: ", args)
        print("Callback function kwargs: ", kwargs)


if __name__ == '__main__':

    # TestGeventPool.run_with_spawn()

    # TestGeventPool.run_with_apply_async()
    # TestGeventPool.run_with_apply()
    # TestGeventPool.run_with_apply_cb()

    # TestGeventPool.run_with_map()
    # TestGeventPool.run_with_map_async()
    # TestGeventPool.run_with_map_cb()
    # TestGeventPool.run_with_map_multiargs()
    TestGeventPool.run_with_map_multiargs_2()

    # TestGeventPool.run_with_imap()
    # TestGeventPool.run_with_imap_unordered()
