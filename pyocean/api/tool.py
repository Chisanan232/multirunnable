from enum import Enum



class Feature(Enum):

    Lock = "lock"
    RLock = "rlock"
    Semaphore = "semaphore"
    Bounded_Semaphore = "bounded_semaphore"
    Event = "event"
    Condition = "condition"

