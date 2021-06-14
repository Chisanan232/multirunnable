import threading

Thread_Number = 5


def function():
    print("This is function content ...")


if __name__ == '__main__':

    threads_list = [threading.Thread(target=function) for _ in range(Thread_Number)]
    for __thread in threads_list:
        __thread.start()

    for __thread in threads_list:
        __thread.join()
