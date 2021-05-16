from .process_factory  import ProcessFactory

from multiprocessing import Pool, JoinableQueue
from multiprocessing.pool import AsyncResult
from typing import List
from datetime import datetime



class ProcessWithJoinableQueue:

    def __init__(self, process_number):
        self.__process_num = process_number
        self.factory = ProcessFactory(process_number=process_number)
        self.queue = JoinableQueue()


    def main(self):
        print(f"Time: {datetime.now()} - This is Main Thread - PID: {os.getpid()}. PPID: {os.getppid()}")
        process_pool = self.factory.init()
        running_process_pool = self.factory.assign_task(pool=process_pool, function=self.process_running_fun)
        self.factory.run_task(pool_list=running_process_pool)


    def init_queue(self):
        pass


    def process_running_fun(self):
        pass



if __name__ == '__main__':

    __process_number = 10

    __test = ProcessWithJoinableQueue(process_number=__process_number)
    __test.main()
