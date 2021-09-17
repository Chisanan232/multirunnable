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
    return "This is fun_1"


async def fun_2(param, index):
    print("This is function_2.")
    print(f"Parameter: {param}")
    sleep_time = random.randrange(1, 10)
    print(f"Func_2 Will sleep for {sleep_time} seconds ... - Async-{index}")
    await asyncio.sleep(sleep_time)
    print(f"Func_2 end, time: {time.time()}")
    return "This is fun_2"



async def run_fun():
    value = await asyncio.gather(fun_1(param="test_1", index="1"), fun_2(param="test_2", index="2"))
    print("value: ", value)



def asyncio_gather():
    asyncio.run(run_fun())



# async def __async_task():
#     _task_1 = asyncio.create_task(fun_1(param="test_1", index="1"))
#     _task_2 = asyncio.create_task(fun_2(param="test_2", index="2"))
#
#     _task_1_val = await _task_1
#     _task_2_val = await _task_2
#
#     print("Return val_1: ", _task_1_val)
#     print("Return val_2: ", _task_2_val)
#
#
# def asyncio_run():
#     asyncio.run(__async_task())



if __name__ == '__main__':

    asyncio_gather()
    # asyncio_run()
