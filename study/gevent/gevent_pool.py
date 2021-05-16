from gevent.pool import Pool
from gevent.threadpool import ThreadPool, ThreadPoolExecutor, Greenlet
# from gevent.thread import Greenlet
from gevent.threading import Thread
from typing import List
import os



class TestGeventPool:

    __Greenlet_List: List[Greenlet] = []

    @classmethod
    def run(cls):
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
    def main_run_fun(cls, index):
        print(f"Run the function with Greenlet! - {index}, pid: {os.getpid()}")
        return "Yee"


if __name__ == '__main__':

    TestGeventPool.run()
