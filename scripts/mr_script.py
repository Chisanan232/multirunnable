from multirunnable import set_mode, RunningMode, SimpleExecutor
from multirunnable.api import retry, RunWith
from multirunnable.factory import BoundedSemaphoreFactory
from multirunnable.adapter.context import context


_Worker_Size = 7
_Semaphore_Value = 2


def target_function_with_bsmp() -> str:
    return retry_success_with_bsmp()


@retry.function
@RunWith.Bounded_Semaphore
def retry_success_with_bsmp() -> str:
    print("Running function ...")
    _worker_name = context.get_current_worker_name()
    return f"{_worker_name} Running Result"


if __name__ == '__main__':

    set_mode(RunningMode.Parallel)

    _bsmp_factory = BoundedSemaphoreFactory(value=_Semaphore_Value)
    _sexor = SimpleExecutor(executors=_Worker_Size)
    _sexor.run(function=target_function_with_bsmp, features=_bsmp_factory)
    _result = _sexor.result()

    for _r in _result:
        print("++++++++++++++++++++++++++++")
        print(f"worker_name: {_r.worker_name}")
        print(f"data: {_r.data}")
        print(f"exception: {_r.exception}")
