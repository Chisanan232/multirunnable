from greenlet import greenlet
from datetime import datetime
from typing import List
import os


class GreenletTest:

    def __init__(self, greenlet_number):
        self.__greenlet_number = greenlet_number


    def test(self):
        # # Basic
        # greenlet_process = greenlet(run=self.running_process)
        # process_run = greenlet_process.run
        # print(f"process_run: {process_run}")
        # greenlet_process.switch()

        # For testing
        greenlet_list = self.generate_greenlets()
        self.activate_greenlet(greenlet_list=greenlet_list)


    def generate_greenlets(self):
        return [greenlet(run=self.running_process) for _ in range(self.__greenlet_number)]


    def activate_greenlet(self, greenlet_list: List[greenlet]):
        for one_greenlet in greenlet_list:
            one_greenlet.switch()


    def running_process(self):
        print(f"This is Greenlet. - PID: {os.getpid()}")


if __name__ == '__main__':

    __greenlet_number = 5

    gl = GreenletTest(greenlet_number=__greenlet_number)
    gl.test()
