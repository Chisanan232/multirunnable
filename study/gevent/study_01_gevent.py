from gevent import greenlet, Greenlet
import gevent
from datetime import datetime
from typing import List
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
        # self.end_greenlet(greenlet_list=greenlet_list)


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
            one_greenlet.kill()


    def running_process(self, index) -> str:
        print(f"This is Greenlet. - PID: {os.getpid()}")
        print(f"This is parameter: {index} - PID: {os.getpid()}")
        return f"index-{index}"


if __name__ == '__main__':

    __greenlet_number = 5

    gl = GeventTest(greenlet_number=__greenlet_number)
    gl.test()
