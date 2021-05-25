
class ThreadsListIsEmptyError(RuntimeError):

    def __str__(self):
        return "It cannot do any operators because of threads-list is empty."
