
class QueueNotExistWithName(RuntimeError):

    def __str__(self):
        return "The queue object doesn't exist with target name."
