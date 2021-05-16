
class GlobalizeObjectError(Exception):

    def __str__(self):
        return "Cannot globalize target object because it is None object."



class GlobalObjectIsNoneError(RuntimeError):

    # def __init__(self, global_object):
    #     self.__global_object = global_object


    def __str__(self):
        return f"Globalized object doesn't be initialized."
