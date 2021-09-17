from gevent import greenlet, Greenlet
import gevent
from datetime import datetime
from typing import List
import random
import time
import os



class GeventTest:

    def __init__(self, greenlet_number):
        self.__greenlet_number = greenlet_number


    def test(self):
        # # Basic
        # greenlet_process = greenlet(run=self.running_process)
        # process_run = greenlet_process.run
        # print(f"process_run: {process_run}")
        # greenlet_process.switch()

        # For testing
        print("Generate Greenlet list.")
        greenlet_list = self.generate_greenlets()
        print("Start to run Greenlet.")
        self.activate_greenlet(greenlet_list=greenlet_list)
        self.end_greenlet(greenlet_list=greenlet_list)


    def generate_greenlets(self) -> List:
        return [gevent.spawn(self.running_process, index) for index in range(self.__greenlet_number)]


    def activate_greenlet(self, greenlet_list: List[Greenlet]) -> None:
        greenlet_list = gevent.joinall(greenlet_list)
        for gl in greenlet_list:
            print(f"value: {gl.value}")
        # for one_greenlet in greenlet_list:
        #     one_greenlet.start()


    def end_greenlet(self, greenlet_list: List[Greenlet]) -> None:
        for one_greenlet in greenlet_list:
            one_greenlet.join()


    def running_process(self, index) -> str:
        print(f"This is Greenlet. - PID: {os.getpid()}")
        print(f"This is parameter: {index} - PID: {os.getpid()}")
        __random_sleep = random.randrange(1, 10)
        print(f"Will sleep for {__random_sleep} seconds.")
        # time.sleep(__random_sleep)
        gevent.sleep(__random_sleep)
        return f"index-{index}"


    def test_init(self):
        __args = ("test_1",)
        __kwargs = {"index": "test_1"}

        print("++++++++++ Greenlet with args ++++++++++")
        __g = gevent.Greenlet(self.running_process, *__args)
        # __g.start()    # Start green-thread but cannot get return value
        __g.run()    # Start green-thread and could get return value
        __g.join()
        __value = __g.value
        __gargs = __g.args
        __gkwargs = __g.kwargs
        __gname = __g.name
        __gexception = __g.exception
        __gstarted = __g.started
        __gloop = __g.loop
        __successful = __g.successful()
        __ready = __g.ready()
        __error = __g.error
        __parent = __g.parent
        __dead = __g.dead
        __gr_frame = __g.gr_frame
        print("value: ", __value)
        print("args: ", __gargs)
        print("kwargs: ", __gkwargs)
        print("name: ", __gname)
        print("exception: ", __gexception)
        print("started: ", __gstarted)
        print("loop: ", __gloop)
        print("successful: ", __successful)
        print("ready: ", __ready)
        print("error: ", __error)
        print("parent: ", __parent)
        print("dead: ", __dead)
        print("gr_frame: ", __gr_frame)

        print("++++++++++ Greenlet with kwargs ++++++++++")
        __g = gevent.Greenlet(self.running_process, **__kwargs)
        __g.start()
        __g.join()


    def test_run(self):
        __args = ("test_1",)
        __kwargs = {"index": "test_1"}

        print("++++++++++ Greenlet with args ++++++++++")
        __g = gevent.Greenlet(self.running_process, *__args)
        __g.run()
        __g.join()


    def test_multi_gthread_run(self):
        __g_result = []

        __args = ("test_1",)
        __kwargs = {"index": "test_1"}

        g_list = [Greenlet(self.running_process, *__args) for _ in range(5)]
        for g in g_list:
            # g.run()
            g.start()

        gevent.joinall(g_list)

        for g in g_list:
            gv = g.value
            __g_result.append(gv)

        # for g in g_list:
        #     g.join()

        print(f"GThread list: {__g_result}")


    def test_multi_gthread_spawn(self):
        __args = ("test_1",)
        __kwargs = {"index": "test_1"}

        g_list = [gevent.spawn(self.running_process, **__kwargs) for _ in range(5)]
        gevent.joinall(g_list)
        g_result_list = [g.value for g in g_list]

        # for g in g_list:
        #     g.join()

        print(f"GThread list: {g_result_list}")



if __name__ == '__main__':

    __greenlet_number = 5

    gl = GeventTest(greenlet_number=__greenlet_number)
    # gl.test()
    gl.test_init()
    # gl.test_run()
    # gl.test_multi_gthread_run()
    # gl.test_multi_gthread_spawn()
