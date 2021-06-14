import threading

Thread_Number = 5


class SampleThread(threading.Thread):

    def run(self):
        print("This is function content which be run in the same time.")


if __name__ == '__main__':

    thread_list = [SampleThread() for _ in range(Thread_Number)]
    for __thread in thread_list:
        __thread.start()

    for __thread in thread_list:
        __thread.join()
