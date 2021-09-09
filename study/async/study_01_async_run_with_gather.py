import asyncio
import random
import time


async def fun_1(param, index):
    print("This is function_1.")
    print(f"Parameter: {param}")
    sleep_time = random.randrange(1, 10)
    print(f"Func_1 Will sleep for {sleep_time} seconds ... - Async-{index}")
    await asyncio.sleep(sleep_time)
    print(f"Func_1 end, time: {time.time()}")


async def fun_2(param, index):
    print("This is function_2.")
    print(f"Parameter: {param}")
    sleep_time = random.randrange(1, 10)
    print(f"Func_2 Will sleep for {sleep_time} seconds ... - Async-{index}")
    await asyncio.sleep(sleep_time)
    print(f"Func_2 end, time: {time.time()}")



async def run_fun():
    await asyncio.gather(fun_1(param="test_1", index="1"), fun_2(param="test_2", index="2"))


if __name__ == '__main__':

    asyncio.run(run_fun())
