from abc import ABCMeta, abstractmethod
import asyncio
import random
import time



class AbstractedAsyncClass(metaclass=ABCMeta):

    def main(self):
        asyncio.run(self.dispatcher())


    async def dispatcher(self):
        self.initialize()
        await asyncio.gather(self.fun_1(params="param_1"), self.fun_2(params="param_2"))


    @abstractmethod
    def initialize(self):
        pass



    @abstractmethod
    def fun_1(self, params):
        pass


    @abstractmethod
    async def fun_2(self, params):
        pass



class AbstractedAdapter(AbstractedAsyncClass):

    @abstractmethod
    async def fun_1(self, params):
        pass



class AsyncImplement1(AbstractedAdapter):

    def initialize(self):
        print("This is initialize process")


    async def fun_1(self, params):
        print("This is function_1.")
        print(f"Parameter: {params}")
        sleep_time = random.randrange(1, 10)
        print(f"Func_1 Will sleep for {sleep_time} seconds ... - Async-1")
        await asyncio.sleep(sleep_time)
        print(f"Func_1 end, time: {time.time()}")


    async def fun_2(self, params):
        print("This is function_2.")
        print(f"Parameter: {params}")
        sleep_time = random.randrange(1, 10)
        print(f"Func_2 Will sleep for {sleep_time} seconds ... - Async-2")
        await asyncio.sleep(sleep_time)
        print(f"Func_2 end, time: {time.time()}")



if __name__ == '__main__':

    _async_implement: AbstractedAsyncClass = AsyncImplement1()
    _async_implement.main()
